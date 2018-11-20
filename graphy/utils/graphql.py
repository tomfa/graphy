from graphene_django.views import GraphQLView
from graphql import GraphQLError

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
        view = super(GraphQLView, cls).as_view(*args, **kwargs)
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
        view = super(GraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((permissions.AllowAny,))(view)
        view = api_view(['GET', 'POST'])(view)
        return view
