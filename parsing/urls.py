from django.urls import path

from . import views

urlpatterns = [
    path('current_page_only', views.current_page_only, name='current'),
    path('all_linked_pages', views.all_linked_pages, name='all'),
    path('test', views.test, name='test')
]