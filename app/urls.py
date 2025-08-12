from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('elements/', views.elements, name='elements'),
    path('left-sidebar/', views.left_sidebar, name='left-sidebar'),
    path('right-sidebar/', views.right_sidebar, name='right-sidebar'),
    path('no-sidebar/', views.no_sidebar, name='no-sidebar'),
]