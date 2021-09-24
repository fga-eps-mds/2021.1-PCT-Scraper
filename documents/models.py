from django.db import models


class Document(models.Model):
    source = models.CharField(max_length=240, blank=False)
    url = models.CharField(max_length=240, blank=False)
    slug = models.CharField(max_length=240)
    title = models.CharField(max_length=240, blank=False)
    content = models.CharField(max_length=2000)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Glossary(models.Model):
    keyword = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
