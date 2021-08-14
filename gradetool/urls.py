from django.urls import path

from .views import GetCSRFToken

urlpatterns = [
    path('csrf_cookie', GetCSRFToken.as_view(), name='csrf_cookie'),
]