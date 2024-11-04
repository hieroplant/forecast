from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Project, Station  

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

def check_project_name(request):
    name = request.GET.get('name', '').upper()
    exists = Project.objects.filter(name__iexact=name).exists()
    return JsonResponse({'exists': exists})

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

def is_valid_sheet_name(sheet_name):
    return (
        sheet_name.startswith("_0") and
        len(sheet_name) <= 5 and
        all(char in "_0123456789" for char in sheet_name)
    )

def extract_station_info(file):
    station_info = []
    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        if is_valid_sheet_name(sheet_name):
            df = pd.read_excel(xls, sheet_name=sheet_name)
            station_info.append((sheet_name, df.iloc[2, 1]))  # Get value from B3
    return station_info

def extract_fail_code_data(file):
    fail_code_data = []
    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        if is_valid_sheet_name(sheet_name):
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # Extract fail code data
            if "Fail Code" in df.iloc[:, 0].values and "Fail Code End" in df.iloc[:, 0].values:
                start_row = df[df.iloc[:, 0].str.contains("Fail Code", na=False)].index[0]
                end_row = df[df.iloc[:, 0].str.contains("Fail Code End", na=False)].index[0]
                fail_code_data.extend(df.iloc[start_row + 1:end_row, 1].tolist())  # Get data from column B
    return fail_code_data

def save_station(project, station_name, station_description):
    Station.objects.get_or_create(
        project=project,
        name=station_name,
        defaults={'description': station_description}
    )

def upload_config(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        config_file = request.FILES.get('config_file')

        if config_file and config_file.name.endswith('.xlsm'):
            # Extract station info from the uploaded file
            station_info_list = extract_station_info(config_file)

            # Save each station information to the database
            for station_name, station_description in station_info_list:
                save_station(project, station_name, station_description)

            # Only extract fail code data if station_info_list has valid data
            if station_info_list:
                fail_code_data_list = extract_fail_code_data(config_file)

                # Process the fail code data as needed
                for fail_code_description in fail_code_data_list:
                    # Here you can save to the database or perform any actions needed
                    pass  # Replace with your saving logic

            return redirect('stations', project_id=project.id)
        else:
            return HttpResponse('Invalid file type', status=400)

    return redirect('stations', project_id=project.id)