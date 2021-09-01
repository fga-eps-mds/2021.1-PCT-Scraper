from django.db import models

class Document(models.Model):
    title = models.CharField("Title", max_length=240)
    url = models.CharField("Url", max_length=1024)
    description = models.CharField("Title", max_length=240)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
