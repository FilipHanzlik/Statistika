from django.db import models

# Create your models here.


class Data(models.Model):
    pohlavi = models.CharField(max_length=5)
    vek = models.IntegerField()
    vyska = models.IntegerField()
    delkaspanku = models.FloatField()
    casvstavani = models.TimeField()
    TypMobilu = models.CharField(max_length=20)
    CasNaSocialnich = models.FloatField(max_length=20)
    SpokojenySeSkolnimSys = models.CharField(max_length=10, default="Ano")

    def __str__(self):
        return f"{self.pohlavi}-{self.vek}"


class Graphs(models.Model):

    class Meta:
        verbose_name_plural = 'graphs'

    vysky_hist = models.CharField(max_length=100000, default='default')
    vysky_cary = models.CharField(max_length=100000)

