from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.main, name="main"),
    path('evaluate', views.evaluate, name="evaluate"),
    path('results', views.results, name="results")
]