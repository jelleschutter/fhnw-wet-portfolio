from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('project/<int:pk>/', views.ProjectView.as_view(), name='project-detail'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag-detail'),
]