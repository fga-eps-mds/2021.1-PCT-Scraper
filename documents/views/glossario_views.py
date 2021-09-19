from rest_framework import viewsets
from documents.serializers import GlossarioSerializer
from documents.models import Glossario


class GlossarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Glossario to be viewed or edited.
    """
    queryset = Glossario.objects.all()
    serializer_class = GlossarioSerializer