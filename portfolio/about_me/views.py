from django.views import generic

from .models import WorkExperience, Skill

class IndexView(generic.base.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work_experiences = WorkExperience.objects.order_by('-start_date')
        context['title'] = 'About Me'
        context['work_experiences'] = work_experiences
        context['skills'] = Skill.objects.order_by('-proficiency')
        return context

class ContactView(generic.base.TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact'
        return context