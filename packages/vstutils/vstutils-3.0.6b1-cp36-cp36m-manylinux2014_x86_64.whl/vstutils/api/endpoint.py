import json
import logging
import traceback
from collections import OrderedDict

from django.conf import settings
from django.db import transaction
from django.test import Client
from drf_yasg.views import SPEC_RENDERERS
from rest_framework import authentication, serializers, views

from . import responses
from .decorators import cache_method_result
from .serializers import DataSerializer
from .validators import UrlQueryStringValidator

logger = logging.getLogger('vstutils')

REST_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'HEAD',
    'OPTIONS'
]


def _join_paths(*args):
    '''Join multiple path fragments into one

    :param *args: List of items that can be anything like '/a/b/c', 'b/c/', 1, 'v1'
    :returns: Path that starts and ends with
    '''
    return f"/{'/'.join(arg.strip('/') for arg in args)}/"


class FormatDataFieldMixin:
    '''Mixin for fields that can format "<< >>" templates inside strings'''

    requires_context = True

    def to_internal_value(self, data):
        result = super().to_internal_value(data)

        if isinstance(result, str) \
                and '<<' in result \
                and '>>' in result \
                and not ('{' in result and '}' in result):
            result = result.replace('<<', '{').replace('>>', '}')
            return result.format(*self.context['results'])
        return result


class TemplateStringField(FormatDataFieldMixin, serializers.CharField):
    pass


class RequestDataField(FormatDataFieldMixin, DataSerializer):
    '''Field that can handle basic data types and recursise format template strings inside them'''

    def to_internal_value(self, data):

        if isinstance(data, (list, tuple)):
            return [self.to_internal_value(i) for i in data]

        elif isinstance(data, (dict, OrderedDict)):
            return type(data)(
                (super(RequestDataField, self).to_internal_value(k), self.to_internal_value(v))
                for k, v in data.items()
            )

        return super(RequestDataField, self).to_internal_value(data)


class MethodChoicesField(serializers.ChoiceField):
    '''Field for HTTP method'''

    def __init__(self, choices=None, **kwargs):
        choices = choices or REST_METHODS
        super().__init__(choices, **kwargs)

    def to_internal_value(self, data):
        return super(MethodChoicesField, self).to_internal_value(str(data).upper())


class PathField(TemplateStringField):

    def to_internal_value(self, data):

        if isinstance(data, str):
            data = (data, )

        return _join_paths(*[
            super(PathField, self).to_internal_value(path)
            for path in data
        ])


class OperationSerializer(serializers.Serializer):
    # pylint: disable=abstract-method
    path = PathField(required=True)
    method = MethodChoicesField(required=True)
    headers = serializers.DictField(child=TemplateStringField(), default={}, write_only=True)
    query = TemplateStringField(required=False, allow_blank=True, default='',
                                validators=[UrlQueryStringValidator()], write_only=True)
    data = RequestDataField(required=False, default=None, allow_null=True)
    version = serializers.ChoiceField(choices=list(settings.API.keys()), default=settings.VST_API_VERSION)
    status = serializers.IntegerField(read_only=True)
    info = serializers.CharField(read_only=True)

    def get_opertaion_method(self, method):
        return getattr(self.context.get('client'), method)

    def _get_rendered(self, response):
        try:
            data = getattr(response, 'data')
            return data
        except:
            pass
        if response.status_code != 404 and getattr(response, "rendered_content", False):  # nocv
            return json.loads(response.rendered_content.decode())
        return dict(detail=str(response.content.decode('utf-8')))

    def create(self, validated_data):
        # pylint: disable=protected-access
        method = self.get_opertaion_method(validated_data['method'].lower())
        url = f"/{settings.API_URL}/{validated_data['version']}/{validated_data['path']}/".replace('//', '/')
        query = validated_data['query']
        if query:
            url += '?' + query
        response = method(
            url,
            content_type='application/json',
            secure=self.context['request']._request.is_secure(),
            data=validated_data['data'],
            **validated_data['headers']
        )
        return dict(
            path=url,
            status=response.status_code,
            data=self._get_rendered(response),
            method=validated_data['method']
        )


class EndpointViewSet(views.APIView):
    schema = None
    renderer_classes = list(views.APIView.renderer_classes) + list(SPEC_RENDERERS)
    session_cookie_name = settings.SESSION_COOKIE_NAME
    client_environ_keys_copy = [
        "SCRIPT_NAME",
        "SERVER_NAME",
        "SERVER_PORT",
        "SERVER_PROTOCOL",
        "SERVER_SOFTWARE",
        "REMOTE_ADDR",
        "HTTP_X_FORWARDED_PROTOCOL",
        "HTTP_HOST",
        "HTTP_USER_AGENT",
    ]

    serializer_class = OperationSerializer

    @cache_method_result
    def get_client(self):
        """Returns test client and guarantees that if bulk request comes
        authenticated than test client will be authenticated with the same user

        :return: test client
        :rtype: django.test.Client
        """
        client = Client(**self.original_environ_data())
        if self.request.user.is_authenticated:
            if isinstance(self.request.successful_authenticator, authentication.SessionAuthentication):
                client.cookies[self.session_cookie_name] = self.request.session.session_key
            else:
                client.force_login(self.request.user)
        return client

    def original_environ_data(self, *args):
        # pylint: disable=protected-access
        get_environ = self.request._request.environ.get
        kwargs = dict()
        for env_var in tuple(self.client_environ_keys_copy) + args:
            value = get_environ(env_var, None)
            if value:
                kwargs[env_var] = str(value)
        return kwargs

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context(kwargs.get('context', {}))
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self, context):
        """
        Extra context provided to the serializer class.
        """
        context = context.copy()
        context.update({
            'request': self.request,
            'view': self
        })
        context['client'] = self.get_client()
        context['results'] = self.results
        return context

    @transaction.atomic()
    def operate(self, operation_data):
        """Method used to handle one operation and return result of it"""
        serializer = self.get_serializer(data=operation_data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except Exception as err:
            return {
                'path': 'bulk',
                'info': getattr(serializer, '_errors', traceback.format_exc()),
                'status': 500,
                'data': dict(detail=f'Error in bulk request data. See info. Original message: {str(err)}')
            }

    def get(self, request, format=None):
        """Returns response with swagger ui or openapi json schema if ?format=openapi"""
        url = '/api/openapi/'

        if request.query_params.get('format') == 'openapi':
            url += '?format=openapi'

        return self.get_client().get(url, secure=request.is_secure())

    def post(self, request):
        """Execute transactional bulk request"""
        try:
            with transaction.atomic():
                return self.put(request, allow_fail=False)
        except Exception:
            logger.debug(traceback.format_exc())
            return responses.HTTP_502_BAD_GATEWAY(self.results)

    def put(self, request, allow_fail=True):
        """Execute non transactionbal bulk request"""
        for operation in request.data:
            result = self.operate(operation)
            self.results.append(result)
            if not allow_fail and not (100 <= result.get('status', 500) < 400):
                raise Exception(f'Execute transaction stopped. Error message: {str(result)}')
        return responses.HTTP_200_OK(self.results)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.results = []

    def finalize_response(self, *args, **kwargs):
        if not isinstance(self.request.successful_authenticator, authentication.SessionAuthentication):
            self.get_client().logout()
        return super().finalize_response(*args, **kwargs)
