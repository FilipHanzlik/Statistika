from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Data, Graphs
from functions import validate_form_input, create_graphs_about_height

def main(request):
    return render(request, 'myapp/main.html')


def evaluate(request):
    form = request.POST

    if request.method == 'POST':
        result_of_validation = validate_form_input(form)
        if result_of_validation[0]:
            Data.objects.create(
                pohlavi=form['pohlavi'],
                vek=form['vek'],
                vyska=form['vyska'],
                delkaspanku=form['delka-spanku'].replace(',', '.'),
                casvstavani=form['cas-vstavani'],
                TypMobilu=form['typ-mobilu'],
                CasNaSocialnich=form['socialni-site'].replace(',', '.'),
                SpokojenySeSkolnimSys=form['skolstvi']
            )
            return HttpResponseRedirect(reverse('myapp:results'))
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
            return render(request, 'myapp/main.html', context)
    else:
        return HttpResponseRedirect(reverse('myapp:results'))


def results(request):
    if not len(Data.objects.all()) < 100:
        num = 20 - len(Data.objects.all())
        if num == 1:
            return render(request, 'myapp/not_enough/jednotny.html')
        elif num < 5:
            return render(request, 'myapp/not_enough/pod_5.html', {'num': num})
        else:
            return render(request, 'myapp/not_enough/5_a_vic.html', {'num': num})

    else:
        if Graphs.objects.all():
            Graphs.objects.all().delete()
        create_graphs_about_height()
        graphs = Graphs.objects.all()
        graphs = graphs[len(graphs) - 1]
        context = {
            'vysky_hist': graphs.vysky_hist,
            'vysky_cary': graphs.vysky_cary
        }
        return render(request, 'myapp/results.html', context=context)
