from django.urls import path

from . import views

urlpatterns = [
    path('submit', views.submit, name='submit'),
    path('update_submission', views.update_submission, name='update_submission'),
    path('grade', views.grade, name='grade'),
    path('get', views.get_submission, name='get_submission'),
    path('get_pages', views.get_submission_pages, name='get_submission_pages'),
    path('page', views.page, name='page'),
    path('comment', views.comment, name='comment'),
    path('get_comments', views.get_comments, name='get_comments'),
    path('test', views.test, name='test')
]