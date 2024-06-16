from django.urls import path

from . import views

app_name = 'about_me'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact')
]