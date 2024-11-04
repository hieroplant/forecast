from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_project/', views.add_project, name='add_project'),
    path('create_project/', views.create_project, name='create_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('stations/<int:project_id>/', views.stations, name='stations'),
    path('check_project_name/', views.check_project_name, name='check_project_name'),
    path('upload_config/<int:project_id>/', views.upload_config, name='upload_config'),
]