from django.contrib import admin

from .models import Project, Tag, ProjectAdmin

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)