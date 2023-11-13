from django.contrib import admin

# Register your models here.
from .models import Task, Tag, Comment, Priority, Status

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Tag)