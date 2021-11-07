from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import datetime
import json

from documents.models import Document


class TestDocumentEndpoint(APITestCase):

    def setUp(self):
        self.url = '/api/documents/'

    def tearDown(self):
        Document.objects.all().delete()

    def test_create_document(self):
        document_data = {
            'source': 'fonte1',
            'url': 'fonte1.com/doc1',
            'slug': 'doc1',
            'title': 'Doc 1',
            'content': 'Content',
            'checksum': '123456789',
            'updated_at': datetime.now()
        }

        response = self.client.post(
            path=self.url,
            data=document_data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            201,
            msg='Failed to create document'
        )

    def test_update_document(self):
        # Create document
        document_data = {
            'source': 'fonte1',
            'url': 'fonte1.com/doc1',
            'slug': 'doc1',
            'title': 'Doc 1',
            'content': 'Content',
            'checksum': '123456789',
            'updated_at': datetime.now()
        }

        Document.objects.create(
            **document_data,
        )

        # Update document
        document_data['title'] = 'Doc 1 [Update]'
        response = self.client.post(
            path=self.url,
            data=document_data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            201,
            msg='Failed to create document'
        )

        # check saved documents
        documents = list(Document.objects.get_queryset())
        self.assertEquals(
            1,
            len(documents),
            msg='Failed to update existing document'
        )

        self.assertEquals(
            document_data['title'],
            documents[0].title,
            msg='Document was not updated'
        )

    def test_list_all_documents(self):
        Document.objects.create(source="fonte1", url="fonte1.com/doc1")

        response = json.loads(self.client.get(
            self.url,
            format='json'
        ).content)

        self.assertEqual(
            1,
            len(response['results']),
        )

    def test_export_search(self):
        Document.objects.create(
            source='fonte1',
            url='fonte1.com/doc1',
            slug='doc1',
            title='Doc 1',
            content='Content',
            checksum='123456789',
            updated_at=datetime.now()
        )

        response = self.client.get(
            '/api/documents/export/'
        )

        self.assertEqual(response.status_code, 200)
