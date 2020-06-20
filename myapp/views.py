from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Data
from functions import validate_form_input
# Create your views here.


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
                delkaspanku=form['delka-spanku'],
                casvstavani=form['cas-vstavani'],
                OSpocitace=form['OS-pocitace'],
                TypMobilu=form['typ-mobilu'],
                CasNaSocialnich=form['socialni-site']
            )
            return HttpResponseRedirect(reverse('myapp:results'))
        else:
            context = {
                'vyska': result_of_validation[1]['vyska'],
                'delka_spanku': result_of_validation[1]['delka_spanku'],
                'cas_vstavani': result_of_validation[1]['cas_vstavani'],
                'socialni_site': result_of_validation[1]['socialni_site'],
                'vyska_prefilled': form['vyska'],
                'delka_spanku_prefilled': form['delka-spanku'],
                'cas_vstavani_prefilled': form['cas-vstavani'],
                'socialne_site_prefilled': form['socialni-site']
            }
            return render(request, 'myapp/main.html', context)
    else:
        return HttpResponseRedirect(reverse('myapp:results'))


def results(request):
    if len(Data.objects.all()) < 20:
        num = 20 - len(Data.objects.all())
        if num == 1:
            return render(request, 'myapp/not_enough/jednotny.html')
        elif num < 5:
            return render(request, 'myapp/not_enough/pod_5.html', {'num': num})
        else:
            return render(request, 'myapp/not_enough/5_a_vic.html', {'num': num})


