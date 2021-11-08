from django.core import paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.utils import paginationProjects, searchProjects
from .forms import ReviewForm, projectForm
from django.db.models import Q 
from .models import Project, Tag


# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    custome_range, projects = paginationProjects(request, projects, 3)
    
    context ={
        'projects':projects,
        'search_query':search_query,
        'paginator':paginator,
        'custome_range':custome_range,
    }
    
    return render(request, 'projects/projects.html', context)


# single project view
def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profiles
            review.save()


            project.getVoteCount
            messages.success(request, 'Your review was successfully submitted')
            return redirect('project', pk=project.id)
            

    context ={
        'project':project,
        'tags':tags,
        'form':form,
        
    }
    return render(request, 'projects/single-project.html', context)


# create project
@login_required(login_url='login')
def createProject(request):
    profile = request.user.profiles
    form = projectForm()

    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES)
        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {
        'form': form,
    }

    return render(request, 'projects/project_form.html', context )

# updating the project
@login_required(login_url='login')
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = projectForm(instance=project)

    if request.method == 'POST':
        form = projectForm(request.POST,request.FILES, instance=project)
        if form.is_valid:
            form.save()
            return redirect('account')
    context = {
        'form': form,
    }

    return render(request, 'projects/project_form.html', context )

# delete project
@login_required(login_url='login')
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {
        'item':project,
    }

    return render(request, 'delete_project.html', context)