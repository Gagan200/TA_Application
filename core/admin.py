from django.contrib import admin
from .models import Course, Application, Comment

admin.site.register(Course)
admin.site.register(Application)
admin.site.register(Comment)