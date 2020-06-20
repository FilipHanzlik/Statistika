from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.test, name="test"),
    path('results', views.evaluate, name="evaluate")
]