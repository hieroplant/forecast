from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Project, Station  # Assuming you have a Station model

def home(request):
    projects = Project.objects.all()
    return render(request, 'siakap/index.html', {'projects': projects})

def add_project(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            name_upper = name.upper()  # Capitalize all letters in the project name
            if Project.objects.filter(name__iexact=name_upper).exists():
                return render(request, 'siakap/createproject.html', {'error': 'Project name already exists'})
            Project.objects.create(name=name_upper, description=description)
            return redirect('home')
        return render(request, 'siakap/createproject.html', {'error': 'Invalid data'})
    return render(request, 'siakap/createproject.html')

def create_project(request):
    return render(request, 'siakap/createproject.html')

def delete_project(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return redirect('home')
    return redirect('home')

def stations(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    stations = Station.objects.filter(project=project)
    return render(request, 'siakap/station.html', {'project': project, 'stations': stations})