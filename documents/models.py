from django.db import models


class Document(models.Model):
    source = models.CharField(max_length=240)
    url = models.CharField(max_length=2000, unique=True)
    slug = models.CharField(max_length=2000)
    title = models.CharField(max_length=2000)
    content = models.TextField()
    checksum = models.CharField(max_length=2000, unique=True)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    classification = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.slug
