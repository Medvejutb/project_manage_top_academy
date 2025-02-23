from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Projects
from ..tasks.models import Tasks
from .forms import TaskForm, Project_create_form

# Create your views here.
def projects_list(request):
    projects = Projects.objects.all()
    return render(request, 'projects/projects_list.html', {'projects': projects})

@login_required
@permission_required('projects.add_task', raise_exception=True)
def project_detail(request, pk):
    project = get_object_or_404(Projects, pk=pk)

    if not (request.user == project.manager or request.user.is_superuser):
        return redirect('projects_list')

    tasks = Tasks.objects.filter(project=project)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', pk=pk)
    else:
        form = TaskForm()

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks':tasks,
        'form': form,
    })

@login_required
@permission_required('projects.add_project', raise_exception=True)
def project_create(request):
    users = User.objects.all()

    if request.method == 'POST':
        form = Project_create_form(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('projects_list')
    else:
        form = Project_create_form()

    return render(request,'projects/project_create.html', {'form': form, 'users': users})