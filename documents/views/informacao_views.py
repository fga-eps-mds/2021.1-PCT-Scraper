from rest_framework import viewsets
from documents.serializers import InformacaoSerializer
from documents.models import Informacao


class InformacaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Informacoes to be viewed or edited.
    """
    queryset = Informacao.objects.all()
    serializer_class = InformacaoSerializer
    # permission_classes = [permissions.IsAuthenticated]