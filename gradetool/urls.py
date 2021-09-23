from django.urls import path

from . import views
from .views import GetCSRFToken

urlpatterns = [
    path('csrf_cookie', GetCSRFToken.as_view(), name='csrf_cookie'),
    path('session', views.session, name='session'),
]