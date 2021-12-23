from django.urls import path

from . import views

app_name = 'rubric'

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('get_by_name', views.get_rubric_by_name, name='get_rubric_by_name'),
    path('get_rubrics', views.get_rubrics, name='get_rubrics'),
    path('get_by_id', views.get_rubric_by_id, name='get_rubric_by_id'),
    path('update', views.update_rubric, name='update_rubric'),
]