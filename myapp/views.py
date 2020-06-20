from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
# Create your views here.


def test(request):
    return render(request, 'myapp/main.html')


def evaluate(request):
    print(request.POST)
    return render(request, 'myapp/results.html')
