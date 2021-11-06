import logging
import pickle

from rest_framework import serializers
from documents.models import Document

from rest_framework.validators import UniqueTogetherValidator


class DocumentSerializer(serializers.ModelSerializer):
    model = pickle.load(open("./documents/model/model.p", "rb"))
    vectorizer = pickle.load(open("./documents/model/vectorizer.p", "rb"))

    class Meta:
        model = Document
        fields = (
            "id",
            "source",
            "url",
            "slug",
            "title",
            "content",
            "checksum",
            "created_at",
            "updated_at",
            "classification"
        )

        extra_kwargs = {
            'url': {
                'validators': []
            },
            'checksum': {
                'validators': []
            }
        }

    def create(self, validated_data):
        logger = logging.getLogger('django')

        try:
            document_queryset = Document.objects.filter(
                url=validated_data.get("url")
            )
        except Document.DoesNotExist:
            document_queryset = None

        document_attributes = {
            "source": validated_data.get("source"),
            "url": validated_data.get("url"),
            "slug": validated_data.get("slug"),
            "title": validated_data.get("title"),
            "content": validated_data.get("content"),
            "checksum": validated_data.get("checksum"),
            "updated_at": validated_data.get("updated_at"),
            "classification": self.get_classification(
                validated_data.get("content")
            ),
        }

        if document_queryset:
            logger.info(f"Updating document {validated_data.get('slug')} ...")
            saved_document = document_queryset.first()

            # Only change updated_at, if checksum changed
            if saved_document.checksum == document_attributes["checksum"]:
                document_attributes["updated_at"] = saved_document.updated_at

            document = document_queryset.update(
                **document_attributes
            )
        else:
            logger.info(f"Saving document {validated_data.get('slug')} ...")
            document = Document.objects.create(
                **document_attributes
            )

        return document

    def get_classification(self, content: str):
        classification_predict = self.model.predict(
            self.vectorizer.transform([content])
        )

        return classification_predict[0] if classification_predict else None
