import json

from django.test import Client
from django.utils import timezone

from rubric.models import Rubric
from submission.models import Submission, Page, Comment

c = Client()

# '''
# To run: run `python manage.py shell < local_tests.py`
r = Rubric(template={'text': {'criteria testing': {'points': 6, 'comments': []}}, 'text 2': {'criteria testing 2': {'points': 8, 'comments': []}}},
           points={'text': {'criteria testing': 6}, 'text 2': {'criteria testing 2': 8}},
           criteria={},
           deadline=timezone.now(),
           upload_time=timezone.now(),
           assignment_name="phase-0")
r.save()

# Create submission
response = c.post('/submission/submit', {"encoded_url": "https%3A//sites.google.com/vt.edu/hci-f19-team-cats/phase-2/system-concept-statement%3Fauthuser%3D0", "group": ["Bob"], "name": "test2", "id": "1"})
print(json.loads(response.content))

# Get pages
response = c.get('/submission/get', {"group_name": "test2", "assignment_name": 'phase-0', "search_term": "phase-2"})

# Create comment
response = c.post('/submission/comment', {'x': 0,
                                          'y': 0,
                                          'text': '[{"text": "", "n": 1}, {"text": "", "n": 1}]', 
                                          'section_name': 'text',
                                          'comments': '{"comment": "testing", "additionalComment": "more testing", "commentPoints": 1, "criteriaName": "criteria testing"}',
                                          'url': '/vt.edu/hci-f19-team-cats/phase-2/system-concept-statement',
                                          'page_name': 'System Concept Statement'})

response = c.post('/submission/comment', {'x': 0,
                                          'y': 0,
                                          'text': '[{"text": "", "n": 1}, {"text": "", "n": 1}]',
                                          'section_name': 'text 2',
                                          'comments': '{"comment": "testing 2", "additionalComment": "more testing 2", "commentPoints": 2, "criteriaName": "criteria testing 2"}',
                                          'url': '/vt.edu/hci-f19-team-cats/phase-2/contextual-inquiry',
                                          'page_name': 'Contextual Inquiry'})
print(json.loads(response.content))
# '''

# Get grade
response = c.get('/submission/grade', {"group_name": "test2", "assignment_name": "phase-0"})