from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('project_detail/<int:pk>/', views.project_detail, name='project_detail'),
    path('project_create', views.project_create, name='project_create')
]