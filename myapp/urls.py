from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.main, name="main"),
    path('form_c', views.form_c, name='form_c'),
    path('form_m', views.form_m, name='form_m'),
    path('evaluate', views.evaluate, name="evaluate"),
    path('results', views.results, name="results")
]
