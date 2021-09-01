from rest_framework import serializers
from pcts_documents.documents.models import Document


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ['title', 'url', 'description', 'created']
