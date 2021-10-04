from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
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

class GlossaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Glossary to be viewed or edited.
    """
    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer

class DocumentByKeyWordViewSet(generics.ListAPIView):
        serializer_class = DocumentSerializer
        http_method_names = ['get']

        def get_queryset(self):
            queryset = Document.objects.all()
            keyword = self.request.GET.get('q', None)
            if keyword is not None:
                        queryset = queryset.filter(
                                Q(url__contains=keyword) |
                                Q(slug__contains=keyword) |
                                Q(title__contains=keyword) |
                                Q(content__contains=keyword)
                            )
            
            return queryset
