from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project-list'),
    path('projects/<slug:slug>/', views.project_detail, name='project-detail'),
    path('contact/', views.contact, name='contact'),
]