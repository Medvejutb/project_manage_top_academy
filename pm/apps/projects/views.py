from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Projects
from ..tasks.models import Tasks
from .forms import TaskForm, Project_create_form

# Create your views here.
def projects_list(request):
    projects = Projects.objects.all()
    user = request.user
    #user_tasks = Tasks.objects.filter(executor=request.user)
    is_admin = user.groups.filter(name='admin').exists()
    is_manager = user.groups.filter(name='manager').exists()
    is_executor = user.groups.filter(name='executor').exists()
    projects_manager = Projects.objects.filter(manager=user)
    projects_executor = Projects.objects.filter(tasks__executor=user).distinct()
    context = {
        'user': user,
        'is_admin': is_admin,
        'is_manager': is_manager,
        'is_executor': is_executor,
        'projects': projects,
        'projects_manager': projects_manager,
        'projects_executor': projects_executor,
    }
    return render(
        request,
        'projects/projects_list.html',
        context
    )

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Projects, pk=pk)

    #if not (request.user == project.manager or request.user.is_superuser):
    #    return redirect('projects_list')

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

    user = request.user
    is_admin = user.groups.filter(name='admin').exists()
    is_manager = user.groups.filter(name='manager').exists()
    is_executor = user.groups.filter(name='executor').exists()

    context = {
        'project': project,
        'tasks': tasks,
        'form': form,
        'is_admin': is_admin,
        'is_manager': is_manager,
        'is_executor': is_executor,
    }

    return render(request, 'projects/project_detail.html', context)

@login_required
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