from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
from documents.serializers import DocumentSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

from documents.models import Document
from django.core import serializers

import logging


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

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

    def create(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        document_url = request.data.get("url")

        try:
            document_queryset = Document.objects.filter(url=document_url)
        except Document.DoesNotExist:
            document_queryset = None

        document_attributes = {
            "source": request.data.get("source"),
            "url": request.data.get("url"),
            "slug": request.data.get("slug"),
            "title": request.data.get("title"),
            "content": request.data.get("content"),
            "checksum": request.data.get("checksum"),
            "updated_at": request.data.get("updated_at"),
        }

        if document_queryset:
            logger.info("Update document")
            saved_document = document_queryset.first()

            # Only change updated_at, if checksum changed
            if saved_document.checksum == document_attributes["checksum"]:
                document_attributes["updated_at"] = saved_document.updated_at

            document_queryset.update(
                **document_attributes
            )
        else:
            logger.info("Save document")
            Document.objects.create(
                **document_attributes
            )

        return Response(status=status.HTTP_201_CREATED)
