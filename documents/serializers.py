from rest_framework import serializers
from documents.models import Informacao, Glossario


class InformacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informacao
        fields = '__all__'
class GlossarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossario
        fields = '__all__'