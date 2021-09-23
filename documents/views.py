from rest_framework import viewsets
from documents.serializers import DocumentSerializer
from documents.serializers import GlossarySerializer

from documents.models import Document
from documents.models import Glossary


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Documents to be viewed or edited.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = [permissions.IsAuthenticated]

class GlossaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Glossary to be viewed or edited.
    """
    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer
