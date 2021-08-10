from django.db import models
from rubric.models import Rubric

# Create your models here.

class Submission(models.Model):
    students = models.JSONField()
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    template = models.JSONField(default=list)
    submitted_url = models.CharField(max_length=256)
    group_name = models.CharField(max_length=128)
    semester = models.CharField(max_length=128)
    upload_time = models.DateTimeField()

class Page(models.Model):
    url = models.CharField(max_length=256)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='page')
    name = models.CharField(max_length=256)
    html = models.TextField()

class Comment(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    text = models.JSONField()
    sectionName = models.CharField(max_length=256)
    points = models.IntegerField()
    commentArray = models.JSONField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments', null=True)
