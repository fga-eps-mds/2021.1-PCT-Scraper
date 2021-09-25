from django.db import models


class Document(models.Model):
    source = models.CharField(max_length=240)
    url = models.CharField(max_length=240)
    slug = models.CharField(max_length=240)
    title = models.CharField(max_length=240)
    content = models.TextField()
    checksum = models.CharField(max_length=240)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Glossary(models.Model):
    keyword = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
