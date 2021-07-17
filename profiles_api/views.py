from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """Test API View"""

    def get(self, request, api_format=None):
        """Return list of API View features"""
        an_api_view = [
            'Uses HTTP methods as function (get, post, put, patch, delete)',
            'Is similar to a traditional django view',
            'Gives you the most control over your application logic',
            'Is mapped manually to urls',
        ]
        return Response({'message': 'Hello!', 'an_api_view': an_api_view})