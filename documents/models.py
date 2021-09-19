from django.db import models

class Informacao(models.Model):
    fonte = models.CharField(max_length=240)
    data_extracao = models.DateField(auto_now_add=True)
    titulo = models.CharField(max_length=240)
    teor_textual = models.CharField(max_length=2000)
    autor = models.CharField(max_length=240)
    dataPublicacao = models.DateField()

    def __str__(self):
        return self.name


class Glossario(models.Model):
    palavra_chave = models.CharField(max_length=240)
    created_at = models.DateField(auto_now_add=True)