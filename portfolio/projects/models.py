from django.db import models
from django.contrib import admin

class Project(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', through='ProjectTag')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField('Project', through='ProjectTag')

    def __str__(self):
        return self.name

class ProjectTag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project.title} tagged with {self.tag.name}'


# --- admin config ---

class TagInline(admin.TabularInline):
    model = Project.tags.through
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = (TagInline,)
