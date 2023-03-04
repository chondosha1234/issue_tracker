from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from issues.models import Issue, Project
from issues.forms import (
    CreateProjectForm, CreateIssueForm,
    UpdateProjectForm, UpdateIssueForm
    )

User = get_user_model()


def home_page(request):
    return redirect('issues:issue_list')


class UserHome(DetailView):
    model = User
    template_name = 'user_home.html'

    def get_context_data(self, **kwargs):
        context = super(UserHome, self).get_context_data(**kwargs)
        context['project_list'] = Project.objects.filter(created_by=self.request.user)
        return context

    def get_object(self):
        return User.objects.get(pk=self.kwargs.get('user_id'))


class UserProfile(DetailView):
    pass


class IssueListView(ListView):
    model = Issue
    template_name = 'issue_list.html'
    paginate_by = 49

    def get_queryset(self):
        if self.kwargs.get('filter_term'):
            filter = self.kwargs.get('filter_term')
            if filter == 'recent':
                return Issue.objects.order_by('-created_on')
            if filter == 'popular':
                return Issue.objects.order_by('-visits')
            if filter == 'open':
                return Issue.objects.filter(issue_status='Open')
            if filter == 'closed':
                return Issue.objects.filter(issue_status='Closed')
            if not filter:
                return Issue.objects.all()
        else:
            return Issue.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IssueListView, self).get_context_data(**kwargs)
        return context


class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issue_details.html'

    def get_object(self):
        return Issue.objects.get(pk=self.kwargs.get('issue_id'))


class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    paginate_by = 49

    def get_queryset(self):
        if self.kwargs.get('filter_term'):
            filter = self.kwargs.get('filter_term')
            if filter == 'recent':
                return Project.objects.order_by('-created_on')
            if filter == 'popular':
                return Project.objects.order_by('-visits')
            if not filter:
                return Project.objects.all()
        else:
            return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        return context


class ProjectDetailView(ListView):
    model = Issue
    template_name = 'project_details.html'
    paginate_by = 49

    def get_queryset(self):
        project = Project.objects.get(pk=self.kwargs.get('project_id'))
        issues = Issue.objects.filter(project=project)

        if self.kwargs.get('filter_term'):
            filter = self.kwargs.get('filter_term')
            if filter == 'open':
                return issues.filter(issue_status='Open').order_by('-created_on')
            if filter == 'closed':
                return issues.filter(issue_status='Closed').order_by('-created_on')
            if not filter:
                return issues.order_by('-created_on')
        else:
            return issues.order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs.get('project_id'))
        return context


@login_required(login_url='accounts:login')
def create_project(request):
    user = request.user
    form = CreateProjectForm(user=user)
    if request.method == 'POST':
        form = CreateProjectForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('issues:user_home', user_id=user.pk)

    context = {
        'form': form,
    }
    return render(request, 'create_project.html', context)


@login_required(login_url='accounts:login')
def update_project(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)
    form = UpdateProjectForm(user=user, instance=project)
    if request.method == 'POST':
        form = UpdateProjectForm(data=request.POST, user=user, instance=project)
        if form.is_valid():
            form.save()
            return redirect('issues:project_details', project_id=project.id)

    context = {
        'form': form,
        'project': project
    }
    return render(request, 'update_project.html', context)


@login_required(login_url='accounts:login')
def delete_project(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        if project.created_by == user:
            project.delete()
            return redirect('issues:user_home', user_id=user.pk)

    return redirect('issues:project_details', project_id=project_id)


@login_required(login_url='accounts:login')
def create_issue(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)
    form = CreateIssueForm(user=user, project=project)
    if request.method == 'POST':
        form = CreateIssueForm(data=request.POST, user=user, project=project)
        if form.is_valid():
            form.save()
            return redirect('issues:project_details', project_id=project.id)
    context = {
        'form': form,
        'project': project
    }
    return render(request, 'create_issue.html', context)


@login_required(login_url='accounts:login')
def update_issue(request, issue_id):
    user = request.user
    issue = Issue.objects.get(id=issue_id)
    project = issue.project
    form = UpdateIssueForm(user=user, project=project, instance=issue)
    if request.method == 'POST':
        form = UpdateIssueForm(data=request.POST, user=user, project=project, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('issues:issue_details', issue_id=issue.id)
    context = {
        'form': form,
        'issue': issue
    }
    return render(request, 'update_issue.html', context)


@login_required(login_url='accounts:login')
def delete_issue(request, issue_id):
    user = request.user
    issue = Issue.objects.get(id=issue_id)
    project = issue.project
    if request.method == 'POST':
        if issue.created_by == user:
            issue.delete()
            return redirect('issues:project_details', project_id=project.id)

    return redirect('issues:issue_details', issue_id=issue.id)
