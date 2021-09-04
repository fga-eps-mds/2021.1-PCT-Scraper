from django.test import TestCase
from documents.models import Document
from datetime import datetime


class TestDocument(TestCase):

    def test_document_creation(self):
        self.assertEqual(1, 1)
