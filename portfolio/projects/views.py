from django.views import generic
from django.db.models import Q

from .models import Project, Tag

class IndexView(generic.base.TemplateView):
    template_name = 'projects/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        context['project_list'] = Project.objects.all()
        context['tag_list'] = Tag.objects.all()
        return context

class ProjectView(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['project'].title
        return context

class TagView(generic.DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['tag'].name
        return context

class SearchView(generic.base.TemplateView):
    template_name = 'projects/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search'
        context['query'] = self.request.GET.get('query')
        if context['query']:
            results = Project.objects.complex_filter(
                Q(title__icontains=context['query']) |
                Q(content__icontains=context['query']) |
                Q(tags__name__icontains=context['query'])
            )
            context['project_list'] = results
        else:
            context['project_list'] = Project.objects.all()
        return context
