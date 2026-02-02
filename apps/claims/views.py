from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Claim
from .serializers import ClaimSerializer

class ClaimViewSet(viewsets.ModelViewSet):
    """
    Public ViewSet for submitting claims.
    List/Retrieve only allows seeing own claims if authenticated, or public create.
    """
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    parser_classes = (MultiPartParser, FormParser) # For file upload

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()] # Only admin can list for now for privacy
