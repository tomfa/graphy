from graphene_django.views import GraphQLView
from graphql import GraphQLError, GraphQLCoreBackend

from rest_framework import (
    permissions,
    request as drf_request,
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.exceptions import AuthenticationFailed


class GraphqlAuthenticationError(GraphQLError):
    pass


def measure_depth(definition, level=1):
    depth = level

    selection_set = getattr(definition, 'selection_set', None)
    if selection_set:
        selections = getattr(definition.selection_set, 'selections', [])
    else:
        selections = getattr(definition, 'selections', [])

    for field in selections:
        if hasattr(field, 'selection_set'):
            new_depth = measure_depth(field.selection_set, level=level + 1)
            if new_depth > depth:
                depth = new_depth
    return depth


class DepthAnalysisBackend(GraphQLCoreBackend):
    MAX_DEPTH = 7

    def document_from_string(self, schema, document_string):
        document = super().document_from_string(schema, document_string)
        ast_definitions = document.document_ast.definitions

        for definition in ast_definitions:
            # We are only interested in queries
            if getattr(definition, 'operation', None) != 'query':
                continue

            depth = measure_depth(definition)
            if depth > self.MAX_DEPTH:
                raise Exception('Query is too complex')

        return document


def auth_required(fn):
    def wrapper(*args, **kwargs):
        *_, info = args

        if not info.context.user.is_authenticated:
            raise GraphqlAuthenticationError('Authentication required.')
        return fn(*args, **kwargs)
    return wrapper


class DRFAuthenticatedGraphQLView(GraphQLView):
    """
    Returns a HTTP 401. Outside GraphQL spec.
    """
    def parse_body(self, request):
        if isinstance(request, drf_request.Request):
            return request.data
        return super().parse_body(request)

    @staticmethod
    def format_error(error):
        if (
                hasattr(error, 'original_error') and
                isinstance(error.original_error, GraphqlAuthenticationError)):
            raise AuthenticationFailed()
        return GraphQLView.format_error(error)

    @classmethod
    def as_view(cls, *args, **kwargs):
        backend = DepthAnalysisBackend()
        view = super(GraphQLView, cls).as_view(backend=backend, *args, **kwargs)
        view = permission_classes((permissions.AllowAny,))(view)
        view = api_view(['GET', 'POST'])(view)
        return view


class AuthenticatedGraphQLView(GraphQLView):
    """
    Returns a regular GraphQL error
    """
    def parse_body(self, request):
        if isinstance(request, drf_request.Request):
            return request.data
        return super().parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        backend = DepthAnalysisBackend()
        view = super(GraphQLView, cls).as_view(backend=backend, *args, **kwargs)
        view = permission_classes((permissions.AllowAny,))(view)
        view = api_view(['GET', 'POST'])(view)
        return view
