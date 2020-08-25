from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Data, Graphs
import pandas as pd
from functions import validate_form_input, create_graphs

def main(request):
    return render(request, 'myapp/get_size.html')

def form_c(request):
    return render(request, 'myapp/form_c.html')

def form_m(request):
    return render(request, 'myapp/form_m.html')

def evaluate(request):
    came_from = request.META['HTTP_REFERER'].split('/')[-1]

    if request.method == 'POST':
        form = request.POST
        result_of_validation = validate_form_input(form)
        if result_of_validation[0]:
            Data.objects.create(
                pohlavi=form['pohlavi'],
                vek=form['vek'],
                vyska=form['vyska'],
                delkaspanku=form['delka-spanku'].replace(',', '.'),
                casvstavani=form['cas-vstavani'],
                TypMobilu=form['typ-mobilu'],
                CasNaSocialnich=form['socialni-site'].replace(',', '.')
            )
            return HttpResponseRedirect(f"results?t={came_from[-1]}")
        else:
            context = {
                'error': True,
                'vyska': result_of_validation[1]['vyska'],
                'delka_spanku': result_of_validation[1]['delka_spanku'],
                'cas_vstavani': result_of_validation[1]['cas_vstavani'],
                'socialni_site': result_of_validation[1]['socialni_site'],
                'vek_prefilled': form['vek'],
                'vyska_prefilled': form['vyska'],
                'delka_spanku_prefilled': form['delka-spanku'],
                'cas_vstavani_prefilled': form['cas-vstavani'],
                'socialne_site_prefilled': form['socialni-site']
            }
            return render(request, f'myapp/{came_from}.html', context)
    else:
        return HttpResponseRedirect(reverse('myapp:main'))


def results(request):
    came_from = request.META['HTTP_REFERER'].split('/')[-1]
    if came_from[:5] == 'form':
        type = came_from[-1]
    else:
        type = request.GET['t']
    df_pohlavi = pd.DataFrame(Data.objects.all().values('pohlavi'))
    if len(df_pohlavi[df_pohlavi['pohlavi'] == 'muz']) < 140 or len(df_pohlavi[df_pohlavi['pohlavi'] == 'zena']) < 14:
        if type == 'm':
            return render(request, 'myapp/not_enought_m.html')
        else:
            return render(request, 'myapp/not_enought_c.html')

    else:
        if Graphs.objects.all():
            Graphs.objects.all().delete()
        create_graphs()
        graphs = Graphs.objects.all()
        graphs = graphs[len(graphs) - 1]
        context = {
            'pohlavi_kolac': graphs.pohlavi_kolac,
            'pohlavi_hist': graphs.pohlavi_hist,
            'vysky_hist': graphs.vysky_hist,
            'vysky_hist_muzi': graphs.vysky_hist_muzi,
            'vysky_hist_zeny': graphs.vysky_hist_zeny,
            'vysky_grafy': graphs.vysky_graph,
            'vysky_grafy_muzi_a_zeny': graphs.vysky_graph_muzi_a_zeny,
            'delky_spanku_hist': graphs.delky_spanku_hist,
            'delky_spanku_hist_muzi': graphs.delky_spanku_hist_muzi,
            'delky_spanku_hist_zeny': graphs.delky_spanku_hist_zeny,
            'delky_spanku_grafy': graphs.delky_spanku_graph,
            'delky_spanku_grafy_muzi_a_zeny': graphs.delky_spanku_graph_muzi_a_zeny,
            'typy_mobilu_kolac': graphs.typy_mobilu_kolac,
            'typy_mobilu_sloupcovy': graphs.typy_mobilu_hist,
            'cas_na_soc_hist_vsichni': graphs.cas_na_soc_hist,
            'cas_na_soc_hist_muzi': graphs.cas_na_soc_hist_muzi,
            'cas_na_soc_hist_zeny': graphs.cas_na_soc_hist_zeny,
            'cas_na_soc_grafy_vsichni': graphs.cas_na_soc_graph,
            'cas_na_soc_grafy_muzi_a_zeny': graphs.cas_na_soc_graph_muzi_a_zeny,
            'cas_vstavani_hist_vsichni': graphs.cas_vstavani_hist,
            'cas_vstavani_hist_muzi': graphs.cas_vstavani_hist_muzi,
            'cas_vstavani_hist_zeny': graphs.cas_vstavani_hist_zeny,
            'cas_vstavani_grafy_vsichni': graphs.cas_vstavani_graph,
            'cas_vstavani_grafy_muzi_a_zeny': graphs.cas_vstavani_graph_muzi_a_zeny
        }
        return render(request, 'myapp/results.html', context=context)
