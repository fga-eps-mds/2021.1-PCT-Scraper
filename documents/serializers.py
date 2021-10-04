from rest_framework import serializers
from documents.models import Document, Glossary


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class GlossarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossary
        fields = '__all__'
