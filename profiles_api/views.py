from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication

from profiles_api import serializers, models, permissions


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, api_format=None):
        """Return list of API View features"""
        an_api_view = [
            'Uses HTTP methods as function (get, post, put, patch, delete)',
            'Is similar to a traditional django view',
            'Gives you the most control over your application logic',
            'Is mapped manually to urls',
        ]
        return Response({'message': 'Hello!', 'an_api_view': an_api_view})

    def post(self, request):
        """Hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""

        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""

        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test api view set"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_view_set = [
            'Uses actions (list, create, retrieve, update, partial_update, destroy)',
            'Automatically maps to urls using routers',
            'more functionality with less code'
        ]
        return Response(
            {
                'message': 'Hello!',
                'a_view_set': a_view_set
            }
        )

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an object by its id"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle partial update"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user auth tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading, updating and deleting of profile feed item"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus,
                          IsAuthenticated)

    def perform_create(self, serializer):
        """sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
