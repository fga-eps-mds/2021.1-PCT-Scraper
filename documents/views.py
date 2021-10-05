from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
from documents.serializers import DocumentSerializer

from documents.models import Document

class DocumentViewSet(generics.ListAPIView):
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
