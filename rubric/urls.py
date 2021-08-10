from django.urls import path

from . import views

app_name = 'rubric'

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('get_by_name', views.get_rubric_by_name, name='get_rubric_by_name')
]