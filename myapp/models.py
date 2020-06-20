from django.db import models

# Create your models here.


class Data(models.Model):
    pohlavi = models.CharField(max_length=5)
    vek = models.IntegerField()
    vyska = models.IntegerField()
    delkaspanku = models.FloatField()
    casvstavani = models.TimeField()
    OSpocitace = models.CharField(max_length=20)
    TypMobilu = models.CharField(max_length=20)
    CasNaSocialnich = models.FloatField(max_length=20)

    def __str__(self):
        return f"{self.pohlavi}-{self.vek}"