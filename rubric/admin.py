from django.contrib import admin
from .models import Rubric

class RubricAdmin(admin.ModelAdmin):
    list_display = ('template', 'points', 'criteria')

# Register your models here.

admin.site.register(Rubric, RubricAdmin)