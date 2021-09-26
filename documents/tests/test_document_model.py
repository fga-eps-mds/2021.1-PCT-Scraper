from django.test import TestCase
from documents.models import Document
from datetime import datetime


class TestDocumentModel(TestCase):

    def test_document_creation(self):
        document_source = "TCU"
        document_url = "https://pesquisa.apps.tcu.gov.br/#/documento/acordao-completo/quilombolas"
        document_slug= "quilombolas",
        document_title = "Quilombolas"
        document_content = "RELATÓRIO DE AUDITORIA"
        document_checksum = "x0f33ab"
        document_updated_at = datetime.now()

        document = Document.objects.create(
            source=document_source,
            url=document_url,
            slug=document_slug,
            title=document_title,
            content=document_content,
            checksum=document_checksum,
            updated_at=document_updated_at,
        )

        self.assertEqual(document_source, document.source)
        self.assertEqual(document_url, document.url)
        self.assertEqual(document_title, document.title)
        self.assertEqual(document_content, document.content)
        self.assertEqual(document_updated_at, document.updated_at)
