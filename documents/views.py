import sys
import os
import logging
import csv

from rest_framework import mixins
from datetime import datetime
from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.request import Request
from django.http import JsonResponse
from rest_framework import status
import pickle
from documents.models import Document
from documents.serializers import DocumentSerializer
from django.core import serializers
from rest_framework import pagination

from rest_framework.decorators import action
from documents.models import Document

from documents.utils import apply_all_filters


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.all()
        date_lte = self.request.GET.get('date-lte', None)
        date_gte = self.request.GET.get('date-gte', None)
        keyword = self.request.GET.get('q', None)
        source = self.request.GET.get('source', None)
        category = self.request.GET.get('category', None)
        order_by = self.request.GET.get('order-by', '-updated_at')

        queryset = apply_all_filters(
            queryset,
            date_lte,
            date_gte,
            source,
            category,
            keyword
        )

        return queryset.order_by(order_by)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={
                'message': 'Document created/updated successfully'
            },
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=False, methods=['get'],
        url_path='predict_classification',
        url_name='get_or_create_consumer_with_schedule')
    def get_or_create_consumer_with_schedule(self, request):
        model = pickle.load(open("./documents/model/model.p", "rb"))
        vectorizer = pickle.load(open("./documents/model/vectorizer.p", "rb"))

        documents = Document.objects.all()
        try:
            for document in documents:
                classification_predict = model.predict(
                    vectorizer.transform([document.content])
                )
                document.classification = classification_predict[0]
                document.save()
            return Response("Ok", status=200)
        except Exception as err:
            return Response(
                f"Failed to predict documents classifications {str(err)}",
                status=400
            )


class DocumentExportCSVViewSet(generics.GenericAPIView):

    def get(self, request: Request, *args, **kwargs):
        date_lte = request.query_params.get('date-lte', None)
        date_gte = request.query_params.get('date-gte', None)
        keyword = request.query_params.get('q', None)
        source = request.query_params.get('source', None)
        category = request.query_params.get('category', None)

        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition':
                ('attachment; '
                 'filename="pcts_busca_export_'
                 f'{self._get_current_datetime()}.csv"'
                 )
            },
        )
        writer = csv.writer(response)
        self._make_header(writer)
        self._make_body(
            writer,
            date_lte,
            date_gte,
            keyword,
            source,
            category
        )

        return response

    def _get_current_datetime(self):
        return datetime.now().\
            replace(second=0, microsecond=0)

    def _make_header(self, writer):
        writer.writerow([
            'Título',
            'Fonte',
            'URL',
            'Classificação',
            'Primeira Coleta',
            'Última Atualização'
        ])

    def _make_body(self, writer, date_lte, date_gte, keyword,
                   source, category):
        documents = Document.objects.all()

        documents = apply_all_filters(
            documents,
            date_lte,
            date_gte,
            source,
            category,
            keyword
        )

        for document in documents:
            writer.writerow([
                document.title,
                document.source,
                document.url,
                document.classification,
                self._get_formatted_date(document.created_at),
                self._get_formatted_date(document.updated_at),
            ])

    def _get_formatted_date(self, document_datetime: datetime):
        return document_datetime.strftime("%d/%m/%Y %H:%M")
