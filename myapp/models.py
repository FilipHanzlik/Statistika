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
        return f"{self.pohlavi}-{self.vek}-{self.TypMobilu}"


class Graphs(models.Model):

    class Meta:
        verbose_name_plural = 'graphs'

    pohlavi_kolac = models.CharField(max_length=100000, default='default')
    pohlavi_hist = models.CharField(max_length=100000, default='default')

    vysky_hist_muzi = models.CharField(max_length=100000, default='default')
    vysky_hist_zeny = models.CharField(max_length=100000, default='default')
    vysky_hist = models.CharField(max_length=100000, default='default')

    vysky_graph = models.CharField(max_length=100000)
    vysky_graph_muzi_a_zeny = models.CharField(max_length=100000, default='default')

    delky_spanku_hist = models.CharField(max_length=100000, default='default')
    delky_spanku_hist_muzi = models.CharField(max_length=100000, default='default')
    delky_spanku_hist_zeny = models.CharField(max_length=100000, default='default')

    delky_spanku_graph = models.CharField(max_length=100000, default='default')
    delky_spanku_graph_muzi_a_zeny = models.CharField(max_length=100000, default='default')

    cas_na_soc_hist = models.CharField(max_length=100000, default='default')
    cas_na_soc_hist_muzi = models.CharField(max_length=100000, default='default')
    cas_na_soc_hist_zeny = models.CharField(max_length=100000, default='default')

    cas_na_soc_graph = models.CharField(max_length=100000, default='default')
    cas_na_soc_graph_muzi_a_zeny = models.CharField(max_length=100000, default='default')

    typy_mobilu_kolac = models.CharField(max_length=100000, default='default')
    typy_mobilu_hist = models.CharField(max_length=100000, default='default')
