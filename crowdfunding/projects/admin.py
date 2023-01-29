from django.contrib import admin

from .models import Pledge, Project
admin.site.register(Project)
admin.site.register(Pledge)

#  Register your models here.
