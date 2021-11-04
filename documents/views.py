from datetime import datetime
from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
from documents.serializers import DocumentSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import pickle
from documents.models import Document
from django.core import serializers

import logging
from rest_framework.decorators import action
from documents.models import Document
import sys
import os


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.all()
        date_lte = self.request.GET.get('date_lte', None)
        date_gte = self.request.GET.get('date_gte', None)
        keyword = self.request.GET.get('q', None)
        source = self.request.GET.get('source', None)
        category = self.request.GET.get('category', None)

        print("TIPO DE DATA")

        queryset = self._filter_by_date(queryset, date_lte, date_gte)
        queryset = self._filter_by_source(queryset, source)
        queryset = self._filter_by_category(queryset, category)
        queryset = self._filter_by_keyword(queryset, keyword)

        return queryset.order_by('-updated_at')

    def _filter_by_date(self, queryset, date_lte, date_gte):
        if date_lte is not None:
            queryset = queryset.filter(
                Q(updated_at__lte=self._convert_to_max_datetime(date_lte))
            )

        if date_gte is not None:
            queryset = queryset.filter(
                Q(updated_at__gte=self._convert_to_min_datetime(date_gte))
            )

        return queryset

    def _filter_by_source(self, queryset, source):
        if source is not None:
            queryset = queryset.filter(
                Q(source=source)
            )
        return queryset

    def _filter_by_category(self, queryset, category):
        if category is not None:
            queryset = queryset.filter(
                Q(classification=category)
            )
        return queryset

    def _filter_by_keyword(self, queryset, keyword):
        if keyword is not None:
            queryset = queryset.filter(
                Q(url__contains=keyword) |
                Q(slug__contains=keyword) |
                Q(title__contains=keyword) |
                Q(content__contains=keyword)
            )

        return queryset

    def _convert_to_max_datetime(self, date):
        # Converte um datetime para o maior
        # horario possivel do dia
        return datetime\
            .fromisoformat(date)\
            .replace(
                minute=59,
                hour=23,
                second=59,
                microsecond=999999
            )

    def _convert_to_min_datetime(self, date):
        # Converte um datetime para o menor
        # horario possivel do dia
        return datetime\
            .fromisoformat(date)\
            .replace(
                minute=0,
                hour=0,
                second=0,
                microsecond=0
            )

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
