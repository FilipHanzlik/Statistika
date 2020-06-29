import numpy as np
import pandas as pd
import io
import urllib, base64
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from myapp.models import Data, Graphs
from django.core.files.images import ImageFile


def validate_form_input(dict):

    # define the result variable (it will be a dict of dicts)
    result = {}
    passed = True  # This variable stores if the test passed

    # test Výška
    try:
        vyska = int(dict['vyska'])
        if vyska <= 220 and vyska >= 50:
            result['vyska'] = 'validate valid'
        else:
            result['vyska'] = 'validate invalid'
            passed = False
    except ValueError:
        result['vyska'] = 'validate invalid'
        passed = False

    # test pro délku spánku
    try:
        delka_spanku = float(dict['delka-spanku'].replace(',', '.'))
        if delka_spanku < 2 or delka_spanku > 20:
            result['delka_spanku'] = 'validate invalid'
            passed = False
        else:
            result['delka_spanku'] = 'validate valid'
    except ValueError:
        result['delka_spanku'] = 'validate invalid'
        passed = False

    # test pro cas vstávaní
    cas_vstavani = dict['cas-vstavani']
    if not isinstance(cas_vstavani, str):
        result['cas_vstavani'] = 'validate invalid'
        passed = False
    else:
        casti = cas_vstavani.split(':')
        if len(casti) == 2 and len(casti[0]) == 2 and len(casti[1]) == 2:
            try:
                if int(casti[0]) > 23:
                    passed = False
                    result['cas_vstavani'] = 'validate invalid'
                elif int(casti[1]) > 59:
                    passed = False
                    result['cas_vstavani'] = 'validate invalid'
                else:
                    result['cas_vstavani'] = 'validate valid'
            except ValueError:
                passed = False
                result['cas_vstavani'] = 'validate invalid'
        else:
            passed = False
            result['cas_vstavani'] = 'validate invalid'

    # test času na sociálních sítích
    try:
        cas_na_soc = float(dict['socialni-site'].replace(',', '.'))
        if cas_na_soc < 20:
            result['socialni_site'] = 'validate valid'
        else:
            result['socialni_site'] = 'validate invalid'
    except ValueError:
        result['socialni_site'] = 'validate invalid'
        passed = False

    return (passed, result)


def create_graphs_about_height():
    df = pd.DataFrame(list(Data.objects.all().values('pohlavi', 'vyska')))

    # uspořádání dat a potřebných proměnných

    vysky = df['vyska'].to_numpy()
    vysky_median, vysky_prumer = np.median(vysky), round(np.mean(vysky), 2)
    vysky_bin = 20
    if abs(vysky_median - vysky_prumer) < 0.5:
        if vysky_median < vysky_prumer:
            vysky_prumer += 0.5 - abs(vysky_median - vysky_prumer)
        else:
            vysky_prumer -= 0.5 - abs(vysky_median - vysky_prumer)

    muzi_vysky = df.loc[df['pohlavi'] == 'muz', ['vyska']]['vyska'].to_numpy()
    muzi_vysky_median, muzi_vysky_prumer = np.median(muzi_vysky), round(np.mean(muzi_vysky), 2)
    muzi_vysky_bin = min(20, len(muzi_vysky) // 2)
    if abs(muzi_vysky_median - muzi_vysky_prumer) < 0.5:
        if muzi_vysky_median < muzi_vysky_prumer:
            muzi_vysky_prumer += 0.5 - abs(muzi_vysky_median - muzi_vysky_prumer)
        else:
            muzi_vysky_prumer -= 0.5 - abs(muzi_vysky_median - muzi_vysky_prumer)

    zeny_vysky = df.loc[df['pohlavi'] == 'zena', ['vyska']]['vyska'].to_numpy()
    zeny_vysky_median, zeny_vysky_prumer = np.median(zeny_vysky), round(np.mean(zeny_vysky), 2)
    zeny_vysky_bin = min(20, len(zeny_vysky) // 2)
    if abs(zeny_vysky_median - zeny_vysky_prumer) < 0.5:
        if zeny_vysky_median < zeny_vysky_prumer:
            zeny_vysky_prumer += 0.5 - abs(zeny_vysky_median - zeny_vysky_prumer)
        else:
            zeny_vysky_prumer -= 0.5 - abs(zeny_vysky_median - zeny_vysky_prumer)

    # histogramy

    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure(figsize=(9, 9))

    # create subplots
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    # histogram muži
    ax1.hist(muzi_vysky, muzi_vysky_bin, rwidth=0.9)
    ax1.axvline(muzi_vysky_prumer, color="red", linestyle="--", label=f"průměr: {muzi_vysky_prumer:.2f} cm")
    ax1.axvline(muzi_vysky_median, color="purple", linestyle="--", label=f"median: {muzi_vysky_median:.2f} cm")
    ax1.set(xlabel="Výška", ylabel="Počet lidí", title="Muži")
    ax1.legend()

    # histogram ženy
    ax2.hist(zeny_vysky, zeny_vysky_bin, rwidth=0.9)
    ax2.axvline(zeny_vysky_prumer, color="red", linestyle="--", label=f"průměr: {zeny_vysky_prumer:.2f} cm")
    ax2.axvline(zeny_vysky_median, color="purple", linestyle="--", label=f"median: {zeny_vysky_median:.2f} cm")
    ax2.set(xlabel="Výška", ylabel="Počet lidí", title="Ženy")
    ax2.legend()

    # histogram všichni
    ax3.hist(vysky, vysky_bin, rwidth=0.9)
    ax3.axvline(vysky_prumer, color="red", linestyle="--", label=f"průměr: {vysky_prumer:.2f} cm")
    ax3.axvline(vysky_median, color="purple", linestyle="--", label=f"median: {vysky_median:.2f} cm")
    ax3.set(xlabel="Výška", ylabel="Počet lidí", title="Všichni")
    ax3.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs = Graphs()
    graphs.vysky_hist = uri

    # křivky

    gs = gridspec.GridSpec(2, 2)

    fig = plt.figure(figsize=(10, 10))

    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, :])

    sns.distplot(muzi_vysky, hist=False, color="blue", label="Muži", kde_kws={'shade': True, 'linewidth': 3}, ax=ax1)
    sns.distplot(zeny_vysky, hist=False, color="red", label="Ženy", kde_kws={'shade': True, 'linewidth': 3}, ax=ax1)
    ax1.set(xlabel="výška (v cm)", ylabel="hustota pravděpodobnosti")

    # sns.distplot(muzi_vysky, hist=False, color="blue", label="Muži", ax=ax2)
    # sns.distplot(zeny_vysky, hist=False, color="red", label="Ženy", ax=ax2)
    sns.distplot(vysky, hist=False, color="green", label="Všichni", ax=ax2, kde_kws={'shade': True, 'linewidth': 3})
    ax2.set(xlabel="výška (v cm)", ylabel="hustota pravděpodobnosti")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.vysky_cary = uri
    graphs.save()
