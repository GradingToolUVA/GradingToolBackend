from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework.parsers import JSONParser
from .serializers import CommentSerializer, SubmissionSerializer

from parsing.parser import Parser
from submission.models import Submission, Page, Comment
from rubric.models import Rubric

import urllib.parse
import json
import pprint

# Create your views here.

def submit(request):
    message = None
    explanation = None
    status_code = 500

    data = json.loads(request.body.decode('utf-8'))

    encoded_url = data['encoded_url']
    url = urllib.parse.unquote(encoded_url)
    group_members = data['group']
    group_name = data['group_name']
    assignment_id = data['assignment_id']

    rubric = get_object_or_404(Rubric, pk=assignment_id)
    template = rubric.template

    upload_time = timezone.now()
    semester = data['semester']

    # if(upload_time.month < 7):
    #     semester = "s" + upload_time.date.year
    # else:
    #     semester = "f" + upload_time.date.year
    # Use the current upload time in the future

    s = Submission(students=group_members, 
                   rubric=rubric,
                   template=template,
                   submitted_url=url,
                   group_name=group_name,
                   semester=semester,
                   upload_time=upload_time)
    s.save()

    p = Parser()
    linked_pages = p.parse_all(url)
    current_page = p.parse(url)

    for page in linked_pages:
        pg = Page(url=page['url'],
                 submission=s,
                 name=page['name'],
                 html=page['html'])
        pg.save()

    current_pg = Page(url=url,
              submission=s,
              name="Landing Page",
              html=current_page)
    current_pg.save()

    message = "Submission created successfully."
    res = {"message": message}
    status_code = 201
    return JsonResponse(res, status=status_code)

def update_submission(request):
    id = request.GET['id']
    submission = Submission.objects.get(pk=id)
    data = JSONParser().parse(request)
    #pprint.pprint(data)
    serializer = SubmissionSerializer(submission, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)

def grade(request):
    message = None
    explanation = None
    status_code = 500

    group_name = request.GET['group_name']
    assignment_name = request.GET['assignment_name']
    submission = Submission.objects.filter(rubric__assignment_name=assignment_name) \
                                   .filter(group_name=group_name) \
                                   .latest('rubric__upload_time')
    # print(submission.id)

    comments = Comment.objects.filter(page__submission__id=submission.id)
    template = submission.template
    reference = submission.rubric.points
    # for p in pages:     
    for c in comments:
        item = c.sectionName
        sub_item = c.comments['criteriaName']
        template[item][sub_item]['points'] += -c.comments['commentPoints']
        template[item][sub_item]['comments'].append(c.comments['comment'])
        template[item][sub_item]['comments'].append(c.comments['additionalComment'])

    submission.template = template
    submission.save()

    print(template)
    print(reference)

    grade = 0
    total = 0
    for item in template:
        for sub_item in template[item]:
            if item not in reference or sub_item not in reference[item]:
                message = 'Rubric Mismatch'
                explanation = 'The rubric applied does not match the rubric attached to the submission.'
                status_code = 400
                res = {"message": message, "explanation": explanation}
                return JsonResponse(res, status=status_code)
            
            grade += template[item][sub_item]['points']
            total += reference[item][sub_item]

    res = {'earned': grade, 'total': total, 'percent': grade/total}

    print(res)

    return JsonResponse(res)

def get_submission(request):
    group_name = request.GET['group_name']
    assignment_name = request.GET['assignment_name']
    semester = request.GET['semester']

    submission = Submission.objects.filter(Q(rubric__assignment_name=assignment_name) &
                                           Q(group_name=group_name) &
                                           Q(semester=semester))
    if submission.count() > 0:
        dict_obj = model_to_dict( submission.latest('upload_time') )
        content = [json.dumps(dict_obj, default=str)]                                      
        res = {"content": content}
        return JsonResponse(res)
    elif submission.count() == 0:
        status_code = 400
        message = 'Invalid Request'
        explanation = "No submission exists with this URL, name, and semester."
        res = {"message": message, "explanation": explanation}
        return JsonResponse(res, status=status_code)

def comment(request):
    message = None
    explanation = None
    status_code = 500

    if request.method == 'GET':
        id = request.GET['id']
        comment = Comment.objects.get(pk=id)
        serializer = CommentSerializer(comment)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        x = data['x']
        y = data['y']
        text = data['text']
        section_name = data['sectionName']
        points = data['points']
        commentArray = data['commentArray']
        id = request.GET['id']
        page = Page.objects.filter(id=id)

        if page.count() == 0:
            status_code = 400
            message = 'Invalid Request'
            explanation = "No webpage exists with this URL and name."
            res = {"message": message, "explanation": explanation}
            return JsonResponse(res, status=status_code)

        if page.count() > 1:
            status_code = 400
            message = 'Invalid Submission'
            explanation = "Duplicate webpages."
            res = {"message": message, "explanation": explanation}
            return JsonResponse(res, status=status_code)

        for p in page:
            c = Comment(x=x,
                        y=y,
                        text=text,
                        sectionName=section_name,
                        points=points,
                        commentArray=commentArray,
                        page=p)
        #print(comments)
        c.save()

        message = "Comment created successfully."
        res = {"message": message, "content": {"id": c.id}}
        status_code = 201
        return JsonResponse(res, status=status_code)

    elif request.method == 'PATCH':
        id = request.GET['id']
        comment = Comment.objects.get(pk=id)
        data = JSONParser().parse(request)
        #pprint.pprint(data)
        serializer = CommentSerializer(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        id = request.GET['id']
        comment = Comment.objects.get(pk=id)
        comment.delete()

        message = "Comment deleted successfully."
        res = {"message": message}
        status_code = 204
        return JsonResponse(res, status=status_code)

def get_comments(request):
    id = request.GET['id']
    comments = Comment.objects.filter(page__id=id)

    content = [] 
    for c in comments:
        content.append(model_to_dict(c))

    res = {"content": content}
    return JsonResponse(res)

def get_submission_pages(request): #gives all pages, and the landing page as well
    group_name = request.GET['group_name']
    assignment_name = request.GET['assignment_name']
    semester = request.GET['semester']
    submission = Submission.objects.filter(rubric__assignment_name=assignment_name) \
                                   .filter(group_name=group_name) \
                                   .filter(semester=semester) \
                                   .latest('upload_time') #get their most recent submission
    
    # for s in submission:
    pages = Page.objects.filter(submission__id=submission.id) 
                      #  .filter(url__icontains=search_term)

    content = []
    for p in pages:
        content.append({"id": p.id,
                        "url": p.url,
                        "name": p.name,
                        "html": p.html})

    res = {"content": content}

    # for c in res['content']:
    #     print(c['url'])
    #     print(c['name'])
    #     print('-'*10)

    return JsonResponse(res)

def test(request):
    return