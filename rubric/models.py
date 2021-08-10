from django.db import models

# Create your models here.

class Rubric(models.Model):
    template = models.JSONField() # An empty grade sheet to fill out as grading goes on
    points = models.JSONField() # Number of points per rubric item/sub item
    criteria = models.JSONField() # Instructions/descriptions for ea rubric item/sub item
    deadline = models.DateField() # Deadline for assignment
    upload_time = models.DateTimeField() # Rubric upload date
    assignment_name = models.CharField(max_length=128, unique=True) # Assignment name
