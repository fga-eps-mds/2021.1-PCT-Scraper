from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from documents.serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows documents to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = DocumentSerializer
    # permission_classes = [permissions.IsAuthenticated]
