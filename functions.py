import numpy as np
import pandas as pd
import io
import urllib, base64
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from myapp.models import Data, Graphs
import datetime

matplotlib.use('Agg')

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


def create_graphs():
    df = pd.DataFrame(list(Data.objects.all().values()))

    ## uspořádání dat a potřebných proměnných

    graphs = Graphs()

    # pohlavi

    pocet_muzu = len(df.loc[df['pohlavi'] == 'muz'])
    pocet_zen = len(df) - pocet_muzu
    procent_muzu = round(pocet_muzu / (pocet_muzu + pocet_zen), 2) * 100
    procent_zen = 100 - procent_muzu
    procenta_pohlavi = [procent_muzu, procent_zen]
    nazvy_kolac_pohlavi = ["Muži", "Ženy"]

    # vysky

    vysky = df['vyska'].to_numpy()
    vysky_median, vysky_prumer = np.median(vysky), round(np.mean(vysky), 2)
    vysky_bin = 20
    if abs(vysky_median - vysky_prumer) < 0.5:
        if vysky_median < vysky_prumer:
            vysky_prumer += 0.5 - abs(vysky_median - vysky_prumer)
        else:
            vysky_prumer -= 0.5 - abs(vysky_median - vysky_prumer)

    muzi_vysky = df.loc[df['pohlavi'] == 'muz', ['vyska']]['vyska'].to_numpy()
    muzi_vysky_median, muzi_vysky_prumer = np.median(muzi_vysky), np.mean(muzi_vysky)
    muzi_vysky_bin = min(20, len(muzi_vysky) // 2)
    if abs(muzi_vysky_median - muzi_vysky_prumer) < 0.5:
        if muzi_vysky_median < muzi_vysky_prumer:
            muzi_vysky_prumer += 0.5 - abs(muzi_vysky_median - muzi_vysky_prumer)
        else:
            muzi_vysky_prumer -= 0.5 - abs(muzi_vysky_median - muzi_vysky_prumer)

    zeny_vysky = df.loc[df['pohlavi'] == 'zena', ['vyska']]['vyska'].to_numpy()
    zeny_vysky_median, zeny_vysky_prumer = np.median(zeny_vysky), np.mean(zeny_vysky)
    zeny_vysky_bin = min(20, len(zeny_vysky) // 2)
    if abs(zeny_vysky_median - zeny_vysky_prumer) < 0.5:
        if zeny_vysky_median < zeny_vysky_prumer:
            zeny_vysky_prumer += 0.5 - abs(zeny_vysky_median - zeny_vysky_prumer)
        else:
            zeny_vysky_prumer -= 0.5 - abs(zeny_vysky_median - zeny_vysky_prumer)

    # delka spanku

    delky_spanku = df['delkaspanku']
    delky_spanku_prumer, delky_spanku_median = np.mean(delky_spanku), np.median(delky_spanku)
    delky_spanku_bin = 20
    if abs(vysky_median - delky_spanku_prumer) < 0.5:
        if delky_spanku_median < delky_spanku_prumer:
            delky_spanku_prumer += 0.5 - abs(delky_spanku_median - delky_spanku_prumer)
        else:
            delky_spanku_prumer -= 0.5 - abs(delky_spanku_median - delky_spanku_prumer)

    delky_spanku_muzi = df.loc[df['pohlavi'] == 'muz', ['delkaspanku']]['delkaspanku'].to_numpy()
    delky_spanku_muzi_prumer, delky_spanku_muzi_median = np.mean(delky_spanku_muzi), np.median(delky_spanku_muzi)
    delky_spanku_muzi_bin = min(20, len(delky_spanku_muzi) // 2)
    if abs(delky_spanku_muzi_median - delky_spanku_muzi_prumer) < 0.5:
        if delky_spanku_muzi_median < delky_spanku_muzi_prumer:
            delky_spanku_muzi_prumer += 0.5 - abs(delky_spanku_muzi_median - delky_spanku_muzi_prumer)
        else:
            delky_spanku_muzi_prumer -= 0.5 - abs(delky_spanku_muzi_median - delky_spanku_muzi_prumer)

    delky_spanku_zeny = df.loc[df['pohlavi'] == 'zena', ['delkaspanku']]['delkaspanku'].to_numpy()
    delky_spanku_zeny_prumer, delky_spanku_zeny_median = np.mean(delky_spanku_zeny), np.median(delky_spanku_zeny)
    delky_spanku_zeny_bin = min(20, len(delky_spanku_zeny) // 2)
    if abs(delky_spanku_zeny_median - delky_spanku_zeny_prumer) < 0.5:
        if delky_spanku_zeny_median < delky_spanku_zeny_prumer:
            delky_spanku_zeny_prumer += 0.5 - abs(delky_spanku_zeny_median - delky_spanku_zeny_prumer)
        else:
            delky_spanku_zeny_prumer -= 0.5 - abs(delky_spanku_zeny_median - delky_spanku_zeny_prumer)

    # kolacovy graf pro typ mobilu

    odpovedi_pro_typy_mobilu = list(df['TypMobilu'].to_numpy())
    typy_mobilu = list(set(odpovedi_pro_typy_mobilu))
    typy_mobilu_a_jejich_pocty = {}

    for typ_mobilu in typy_mobilu:
        typy_mobilu_a_jejich_pocty[typ_mobilu] = odpovedi_pro_typy_mobilu.count(typ_mobilu)

    print()

    nazvy_typy_mobilu = sorted(typy_mobilu_a_jejich_pocty, key=typy_mobilu_a_jejich_pocty.get, reverse=True) # seřadí slovník podle počtu výskytů a vrátí seznam názvů
    serazeni_typy_mobilu = nazvy_typy_mobilu[:]
    procenta_typy_mobilu = []

    for typ_mobilu in nazvy_typy_mobilu:
        procenta_typy_mobilu.append(round((typy_mobilu_a_jejich_pocty[typ_mobilu] / sum(typy_mobilu_a_jejich_pocty.values()))*100, 2))
    for i in range(len(nazvy_typy_mobilu)):
        nazvy_typy_mobilu[i] = f"{nazvy_typy_mobilu[i]} ({procenta_typy_mobilu[i]}%)"
    print('---------------')
    print(serazeni_typy_mobilu)
    print(typy_mobilu_a_jejich_pocty)
    print(procenta_typy_mobilu)
    print('---------------')
    print()

    # Cas na soc. sítích všichni

    cas_na_soc = df['CasNaSocialnich']
    cas_na_soc_prumer, cas_na_soc_median = np.mean(cas_na_soc), np.median(cas_na_soc)
    cas_na_soc_bin = 20
    if abs(cas_na_soc_median - cas_na_soc_prumer) < 0.5:
        if cas_na_soc_median < cas_na_soc_prumer:
            cas_na_soc_prumer += 0.5 - abs(cas_na_soc_median - cas_na_soc_prumer)
        else:
            cas_na_soc_prumer -= 0.5 - abs(cas_na_soc_median - cas_na_soc_prumer)

    # Čas na soc. sítích muži

    cas_na_soc_muzi = df.loc[df['pohlavi'] == 'muz', ['CasNaSocialnich']]['CasNaSocialnich'].to_numpy()
    cas_na_soc_muzi_prumer, cas_na_soc_muzi_median = np.mean(cas_na_soc_muzi), np.median(cas_na_soc_muzi)
    cas_na_soc_muzi_bin = min(20, len(cas_na_soc_muzi) // 2)
    if abs(cas_na_soc_muzi_median - cas_na_soc_muzi_prumer) < 0.5:
        if cas_na_soc_muzi_median < cas_na_soc_muzi_prumer:
            cas_na_soc_muzi_prumer += 0.5 - abs(cas_na_soc_muzi_median - cas_na_soc_muzi_prumer)
        else:
            cas_na_soc_muzi_prumer -= 0.5 - abs(cas_na_soc_muzi_median - cas_na_soc_muzi_prumer)

    # Čas na soc. sítích ženy

    cas_na_soc_zeny = df.loc[df['pohlavi'] == 'zena', ['CasNaSocialnich']]['CasNaSocialnich'].to_numpy()
    cas_na_soc_zeny_prumer, cas_na_soc_zeny_median = np.mean(cas_na_soc_zeny), np.median(cas_na_soc_zeny)
    cas_na_soc_zeny_bin = min(20, len(cas_na_soc_zeny) // 2)
    if abs(cas_na_soc_zeny_median - cas_na_soc_zeny_prumer) < 0.5:
        if cas_na_soc_zeny_median < cas_na_soc_zeny_prumer:
            cas_na_soc_zeny_prumer += 0.5 - abs(cas_na_soc_zeny_median - cas_na_soc_zeny_prumer)
        else:
            cas_na_soc_zeny_prumer -= 0.5 - abs(cas_na_soc_zeny_median - cas_na_soc_zeny_prumer)

    # casy vstavani

    casy_vstavani_bez_datumu = df['casvstavani']
    tday = datetime.date.today()
    casy_vstavani = [datetime.datetime(tday.year, tday.month, tday.day, cas.hour, cas.minute, cas.second) for cas in casy_vstavani_bez_datumu]
    print(casy_vstavani)

    ## grafy

    # kolacovy graf pohlavi
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(procenta_pohlavi, labels=nazvy_kolac_pohlavi, shadow=True, explode=[0.05, 0], startangle=90, autopct="%1.1f%%")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.pohlavi_kolac = uri
    plt.close(fig)

    # sloupcovi graf pohlavi pohlavi

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.bar(["Muži", "Ženy"], [pocet_muzu, pocet_zen], color=["blue", "orange"])
    ax.set(ylabel="Počet lidí")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.pohlavi_hist = uri
    plt.close(fig)

    # histogram vysky muži

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(muzi_vysky, muzi_vysky_bin, rwidth=0.9)
    ax.axvline(muzi_vysky_prumer, color="red", linestyle="--", label=f"průměr: {muzi_vysky_prumer:.2f} cm")
    ax.axvline(muzi_vysky_median, color="purple", linestyle="--", label=f"median: {muzi_vysky_median:.2f} cm")
    ax.set(xlabel="Výška (v cm)", ylabel="Počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.vysky_hist_muzi = uri
    plt.close(fig)

    # histogram vysky ženy

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(zeny_vysky, zeny_vysky_bin, rwidth=0.9)
    ax.axvline(zeny_vysky_prumer, color="red", linestyle="--", label=f"průměr: {zeny_vysky_prumer:.2f} cm")
    ax.axvline(zeny_vysky_median, color="purple", linestyle="--", label=f"median: {zeny_vysky_median:.2f} cm")
    ax.set(xlabel="Výška (v cm)", ylabel="Počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.vysky_hist_zeny = uri
    plt.close(fig)

    # histogram všichni
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(vysky, vysky_bin, rwidth=0.9)
    ax.axvline(vysky_prumer, color="red", linestyle="--", label=f"průměr: {vysky_prumer:.2f} cm")
    ax.axvline(vysky_median, color="purple", linestyle="--", label=f"median: {vysky_median:.2f} cm")
    ax.set(xlabel="Výška (v cm)", ylabel="Počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.vysky_hist = uri
    plt.close(fig)

    # křivky výšky všichni

    fig, ax = plt.subplots(figsize=(10, 10))

    sns.distplot(vysky, hist=False, color="green", label="Všichni", ax=ax, kde_kws={'shade': True, 'linewidth': 3})
    ax.set(xlabel="výška (v cm)", ylabel="hustota pravděpodobnosti")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.vysky_graph = uri
    plt.close(fig)

    # křivky výšky muži a ženy

    fig, ax = plt.subplots(figsize=(10, 10))

    sns.distplot(muzi_vysky, hist=False, color="blue", label="Muži", kde_kws={'shade': True, 'linewidth': 3}, ax=ax)
    sns.distplot(zeny_vysky, hist=False, color="red", label="Ženy", kde_kws={'shade': True, 'linewidth': 3}, ax=ax)
    ax.set(xlabel="výška (v cm)", ylabel="hustota pravděpodobnosti")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.vysky_graph_muzi_a_zeny = uri
    plt.close(fig)

    # delka_spanku histopgramy všichni

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.hist(delky_spanku, delky_spanku_bin, rwidth=0.95)
    ax.axvline(delky_spanku_prumer, color="red", linestyle="--", label=f"průměr: {delky_spanku_prumer:.2f}")
    ax.axvline(delky_spanku_median, color="purple", linestyle="--", label=f"median: {delky_spanku_median:.2f}")
    ax.set(xlabel="hodiny", ylabel="počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.delky_spanku_hist = uri
    plt.close(fig)

    # delka_spanku histopgramy muži

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.hist(delky_spanku_muzi, delky_spanku_muzi_bin, rwidth=0.95)
    ax.axvline(delky_spanku_muzi_prumer, color="red", linestyle="--", label=f"průměr: {delky_spanku_muzi_prumer:.2f}")
    ax.axvline(delky_spanku_muzi_median, color="purple", linestyle="--", label=f"median: {delky_spanku_muzi_median:.2f}")
    ax.set(xlabel="hodiny", ylabel="počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.delky_spanku_hist_muzi = uri
    plt.close(fig)

    # delka_spanku histopgramy ženy

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.hist(delky_spanku_zeny, delky_spanku_zeny_bin, rwidth=0.95)
    ax.axvline(delky_spanku_zeny_prumer, color="red", linestyle="--", label=f"Průměr: {delky_spanku_zeny_prumer:.2f}")
    ax.axvline(delky_spanku_zeny_median, color="purple", linestyle="--", label=f"Median: {delky_spanku_zeny_median:.2f}")
    ax.set(xlabel="hodiny", ylabel="počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.delky_spanku_hist_zeny = uri
    plt.close(fig)


    # delka spanku grafy všichni

    fig, ax = plt.subplots(figsize=(10, 10))

    sns.distplot(delky_spanku, hist=False, kde_kws={'shade': True, 'linewidth': 3}, label="Všichni", color="green", ax=ax)
    ax.set(xlabel="hodiny", ylabel="hustota pravděpodobnosti")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.delky_spanku_graph = uri
    plt.close(fig)


    # delky spanku grafy muži a ženy

    fig, ax = plt.subplots(figsize=(10, 10))

    sns.distplot(delky_spanku_muzi, hist=False, kde_kws={'shade': True, 'linewidth': 3}, label='Muži', color="blue", ax=ax)
    sns.distplot(delky_spanku_zeny, hist=False, kde_kws={'shade': True, 'linewidth': 3}, label='Ženy', color="red", ax=ax)
    ax.set(xlabel="hodiny", ylabel="hustota pravděpodobnosti")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.delky_spanku_graph_muzi_a_zeny = uri
    plt.close(fig)


    # typy mobilů koláčový graf

    if len(nazvy_typy_mobilu) > 2:
        fig = plt.figure(figsize=(5, 5))
        patches, texts = plt.pie(procenta_typy_mobilu)
        plt.legend(patches, nazvy_typy_mobilu)

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
    else:
        fig, ax = plt.figure(figsize=(5, 5))
        ax.pie(procenta_typy_mobilu, labels=serazeni_typy_mobilu, shadow=True, explode=[0.5, 0][:len(nazvy_typy_mobilu)], startangle=90, autopct="%1.1f%%")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

    graphs.typy_mobilu_kolac = uri
    plt.close(fig)

    # typy mobilu sloupcovy graf

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.bar(serazeni_typy_mobilu, [typy_mobilu_a_jejich_pocty[typ_mobilu] for typ_mobilu in serazeni_typy_mobilu],
           color=["blue", "orange", "green", "red"][:len(serazeni_typy_mobilu)])

    ax.set(ylabel="počet lidí")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    graphs.typy_mobilu_hist = uri
    plt.close(fig)


    # histogramy cas na socialnich sitích všichni

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(cas_na_soc, cas_na_soc_bin, rwidth=0.95)
    ax.axvline(cas_na_soc_prumer, color="red", linestyle='--', label=f"Průměr: {cas_na_soc_prumer:.2f}")
    ax.axvline(cas_na_soc_median, color="blue", linestyle='--', label=f"Median: {cas_na_soc_median:.2f}")
    ax.set(xlabel="Čas strávení na sociálních sítích v hodinách", ylabel="počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode((buf.read()))
    uri = urllib.parse.quote(string)

    graphs.cas_na_soc_hist = uri
    plt.close(fig)


    # histogramy cas na socialnich sitích muži

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(cas_na_soc_muzi, cas_na_soc_muzi_bin, rwidth=0.95)
    ax.axvline(cas_na_soc_muzi_prumer, color="red", linestyle='--', label=f"Průměr: {cas_na_soc_muzi_prumer:.2f}")
    ax.axvline(cas_na_soc_muzi_median, color="blue", linestyle='--', label=f"Median: {cas_na_soc_muzi_median:.2f}")
    ax.set(xlabel="Čas strávení na sociálních sítích v hodinách", ylabel="počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode((buf.read()))
    uri = urllib.parse.quote(string)

    graphs.cas_na_soc_hist_muzi = uri
    plt.close(fig)


    # histogramy cas na socialnich sitích ženy

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(cas_na_soc_zeny, cas_na_soc_zeny_bin, rwidth=0.95)
    ax.axvline(cas_na_soc_zeny_prumer, color="red", linestyle='--', label=f"Průměr: {cas_na_soc_zeny_prumer:.2f}")
    ax.axvline(cas_na_soc_zeny_median, color="blue", linestyle='--', label=f"Median: {cas_na_soc_zeny_median:.2f}")
    ax.set(xlabel="Čas strávení na sociálních sítích v hodinách", ylabel="počet lidí")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode((buf.read()))
    uri = urllib.parse.quote(string)

    graphs.cas_na_soc_hist_zeny = uri
    plt.close(fig)

    # grafy cas na socialnich sitích vsichni

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.distplot(cas_na_soc, hist=False, kde_kws={'shade': True, 'linewidth': 3}, label='Všichni', color="green", ax=ax)
    ax.set(ylabel='Hustota pravděpodobnosti', xlabel="Čas strávení na sociálních sítích v hodinách")
    ax.set_xlim(left=0)
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode((buf.read()))
    uri = urllib.parse.quote(string)

    graphs.cas_na_soc_graph = uri
    plt.close(fig)

    # grafy cas na socialnich sitích muži a ženy

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.distplot(cas_na_soc_muzi, hist=False, kde_kws={'shade': True, 'linewidth': 3}, label='Muži', color="blue", ax=ax)
    sns.distplot(cas_na_soc_zeny, hist=False, kde_kws={'shade': True, 'linewidth': 3}, label='Ženy', color="red", ax=ax)
    ax.set(ylabel='Hustota pravděpodobnosti', xlabel="Čas strávení na sociálních sítích v hodinách")
    ax.set_xlim(left=0)
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode((buf.read()))
    uri = urllib.parse.quote(string)

    graphs.cas_na_soc_graph_muzi_a_zeny = uri
    plt.close(fig)

    graphs.save()
