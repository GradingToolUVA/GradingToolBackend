from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import json
# Create your views here.

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    def get(self, request, format=None):
        return Response({ 'success': 'CSRF cookie set' })

def session(request):
    if request.method == 'GET':
        res = {"content": request.session.get('last_session')}
        return JsonResponse(res)

    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        request.session['last_session'] = data['last_session']
        return JsonResponse({ 'success': 'last session stored' })