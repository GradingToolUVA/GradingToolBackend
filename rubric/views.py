from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.forms.models import model_to_dict
from rest_framework.parsers import JSONParser
from .serializers import RubricSerializer
from .models import Rubric

from rest_framework import viewsets
import datetime
import json

# TODO: Catch key errors
def upload(request):
    data = json.loads(request.body.decode('utf-8'))
    template = data['template']
    year = data['year']
    month = data['month']
    day = data['day']
    hour = data['hour']
    minute = data['minute']
    name = data['name']

    r = Rubric(template=template,
               deadline=datetime.datetime(year, month, day, hour, minute),
               upload_time=timezone.now(),
               assignment_name=name)
    r.save()

    res = {"message": "Assignment submitted successfully."}
    return JsonResponse(res)

def get_rubric_by_name(request):
    assignment_name = request.GET['assignment_name']
    rubric = Rubric.objects.filter(assignment_name=assignment_name)
    rubric = rubric.latest('upload_time')

    dict_obj = model_to_dict( rubric )
    rubricJSON = json.dumps(dict_obj, default=str)

    res = {"content": [{"id": rubric.id, "rubric": rubricJSON}]}
    return JsonResponse(res)

def get_rubrics(request):
    rubrics = Rubric.objects.all()

    content = [] 
    for r in rubrics:
        content.append(model_to_dict(r))

    res = {"content": content}
    return JsonResponse(res)

def get_rubric_by_id(request):
    id = request.GET['id']
    rubric = Rubric.objects.get(id=id)

    dict_obj = model_to_dict( rubric )
    rubricJSON = json.dumps(dict_obj, default=str)

    res = {"content": {"rubric": rubricJSON}}
    return JsonResponse(res)

def update_rubric(request):
    id = request.GET['id']
    rubric = Rubric.objects.get(pk=id)
    data = JSONParser().parse(request)
    #pprint.pprint(data)
    serializer = RubricSerializer(rubric, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)