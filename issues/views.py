from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model

from issues.models import Issue, Project, Comment
from issues.forms import (
    CreateProjectForm, CreateIssueForm,
    UpdateProjectForm, UpdateIssueForm,
    AddUserForm, SearchForm,
    CommentForm
    )

User = get_user_model()


def home_page(request):
    if request.user.is_authenticated:
        return redirect('issues:user_home', user_id=request.user.pk)
    else:
        return redirect('issues:issue_list')


def search(request):
    form = SearchForm()
    results = []

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            results.extend(Project.objects.filter(title__icontains=search_query))
            results.extend(Issue.objects.filter(title__icontains=search_query))
            results.extend(User.objects.filter(email__icontains=search_query))

    context = {
        'search_form': form,
        'results': results,
        'project_sidebar_list': project_sidebar_list,
        'issue_sidebar_list': issue_sidebar_list
    }
    get_sidebar_context(request.user, context)
    return render(request, 'search.html', context)


class UserHome(DetailView):
    model = User
    template_name = 'user_home.html'

    def get_context_data(self, **kwargs):
        context = super(UserHome, self).get_context_data(**kwargs)
        projects = self.request.user.projects_assigned.all()
        context['project_list'] = projects
        context['project_sidebar_list'] = projects.order_by('-modified_on')[:5]
        context['issue_sidebar_list'] = self.request.user.issues_assigned.all().order_by('-modified_on')[:5]
        return context

    def get_object(self):
        return User.objects.get(pk=self.kwargs.get('user_id'))


class UserProfile(DetailView):
    pass


class IssueListView(ListView):
    model = Issue
    template_name = 'issue_list.html'
    paginate_by = 10
    page_range_displayed = 8

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
        get_sidebar_context(self.request.user, context)

        paginator = context['paginator']
        page = context['page_obj']
        context['current_page'] = page.number
        context['total_pages'] = paginator.num_pages

        start_page = max(page.number - self.page_range_displayed//2, 1)
        end_page = min(page.number + self.page_range_displayed//2, paginator.num_pages)
        context['page_range'] = range(start_page, end_page+1)
        
        context['search_form'] = SearchForm()
        context['filter_term'] = self.kwargs.get('filter_term')
        return context


class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issue_details.html'

    def get_object(self):
        issue = Issue.objects.get(pk=self.kwargs.get('issue_id'))
        issue.visits += 1
        issue.save()
        return issue

    def get_all_comment_forms(self, issue):
        comments = Comment.objects.filter(issue=issue)
        forms = {}
        for comment in comments:
            forms[comment.id] = CommentForm(user=self.request.user, issue=issue, instance=comment)
        return forms

    def get_context_data(self, **kwargs):
        context = super(IssueDetailView, self).get_context_data(**kwargs)
        get_sidebar_context(self.request.user, context)

        issue = Issue.objects.get(pk=self.kwargs.get('issue_id'))
        top_level_comments = Comment.objects.filter(issue=issue).filter(parent_comment=None)

        context['comment_list'] = top_level_comments
        context['edit_forms'] = self.get_all_comment_forms(issue)
        context['search_form'] = SearchForm()
        context['user_form'] = AddUserForm()
        context['comment_form'] = CommentForm(user=self.request.user, issue=issue)
        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    paginate_by = 10
    page_range_displayed = 8

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
        get_sidebar_context(self.request.user, context)

        paginator = context['paginator']
        page = context['page_obj']
        context['current_page'] = page.number
        context['total_pages'] = paginator.num_pages

        start_page = max(page.number - self.page_range_displayed//2, 1)
        end_page = min(page.number + self.page_range_displayed//2, paginator.num_pages)
        context['page_range'] = range(start_page, end_page+1)

        context['search_form'] = SearchForm()
        context['filter_term'] = self.kwargs.get('filter_term')
        return context


class ProjectDetailView(ListView):
    model = Issue
    template_name = 'project_details.html'
    paginate_by = 10
    page_range_displayed = 8

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
        get_sidebar_context(self.request.user, context)

        project = Project.objects.get(pk=self.kwargs.get('project_id'))
        project.visits += 1
        project.save()

        paginator = context['paginator']
        page = context['page_obj']
        context['current_page'] = page.number
        context['total_pages'] = paginator.num_pages

        start_page = max(page.number - self.page_range_displayed//2, 1)
        end_page = min(page.number + self.page_range_displayed//2, paginator.num_pages)
        context['page_range'] = range(start_page, end_page+1)

        context['project'] = project
        context['search_form'] = SearchForm()
        context['user_form'] = AddUserForm()
        return context


@login_required(login_url='login')
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
    get_sidebar_context(request.user, context)
    return render(request, 'create_project.html', context)


@login_required(login_url='login')
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
    get_sidebar_context(request.user, context)
    return render(request, 'update_project.html', context)


@login_required(login_url='login')
def delete_project(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        if project.created_by == user:
            project.delete()
            return redirect('issues:user_home', user_id=user.pk)

    return redirect('issues:project_details', project_id=project_id)


@login_required(login_url='login')
def add_user_to_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(name=username)
            project.assigned_users.add(user)
            project.save()
            return redirect('issues:project_details', project_id=project.id)

    return redirect('issues:project_details', project_id=project.id)


@login_required(login_url='login')
def remove_user_from_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(name=username)
            project.assigned_users.remove(user)
            project.save()
            return redirect('issues:project_details', project_id=project.id)

    return redirect('issues:project_details', project_id=project.id)


@login_required(login_url='login')
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
    get_sidebar_context(request.user, context)
    return render(request, 'create_issue.html', context)


@login_required(login_url='login')
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
    get_sidebar_context(request.user, context)
    return render(request, 'update_issue.html', context)


@login_required(login_url='login')
def delete_issue(request, issue_id):
    user = request.user
    issue = Issue.objects.get(id=issue_id)
    project = issue.project
    if request.method == 'POST':
        if issue.created_by == user:
            issue.delete()
            return redirect('issues:project_details', project_id=project.id)

    return redirect('issues:issue_details', issue_id=issue.id)


@login_required(login_url='login')
def add_user_to_issue(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(name=username)
            issue.assigned_users.add(user)
            issue.save()
            return redirect('issues:issue_details', issue_id=issue.id)

    return redirect('issues:issue_details', issue_id=issue.id)


@login_required(login_url='login')
def remove_user_from_issue(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(name=username)
            issue.assigned_users.remove(user)
            issue.save()
            return redirect('issues:issue_details', issue_id=issue.id)

    return redirect('issues:issue_details', issue_id=issue.id)


@login_required(login_url='login')
def open_issue(request, issue_id):
    user = request.user
    issue = Issue.objects.get(id=issue_id)
    if request.method == 'POST':
        if issue.issue_status == 'Closed' and user in issue.assigned_users.all():
            issue.issue_status = 'Open'
            issue.save()
            return redirect('issues:issue_details', issue_id=issue.id)

    return redirect('issues:issue_details', issue_id=issue.id)


@login_required(login_url='login')
def close_issue(request, issue_id):
    user = request.user
    issue = Issue.objects.get(id=issue_id)
    if request.method == 'POST':
        if issue.issue_status == 'Open' and user in issue.assigned_users.all():
            issue.issue_status = 'Closed'
            issue.save()
            return redirect('issues:issue_details', issue_id=issue.id)

    return redirect('issues:issue_details', issue_id=issue.id)


@login_required(login_url='login')
def add_comment(request, issue_id, parent_id=None):
    user = request.user
    issue = Issue.objects.get(id=issue_id)
    if parent_id:
        parent_comment = Comment.objects.get(id=parent_id)
    else:
        parent_comment = None

    if request.method == 'POST':
        form = CommentForm(data=request.POST, user=user, issue=issue, parent=parent_comment)
        if form.is_valid():
            form.save()
            return redirect('issues:issue_details', issue_id=issue.id)

    return redirect('issues:issue_details', issue_id=issue.id)


@login_required(login_url='login')
def edit_comment(request, comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id)
    issue = comment.issue
    if request.method == 'POST':
        form = CommentForm(data=request.POST, user=user, issue=issue, parent=comment.parent_comment, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('issues:issue_details', issue_id=issue.id)

    return redirect('issues:issue_details', issue_id=issue.id)


@login_required(login_url='login')
def delete_comment(request, comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id)
    issue = comment.issue
    if request.method == 'POST':
        if user == comment.user:
            comment.delete()
            return redirect('issues:issue_details', issue_id=issue.id)

    return redirect('issues:issue_details', issue_id=issue.id)


def get_sidebar_context(user, context):
    if user.is_authenticated:
        context['project_sidebar_list'] = user.projects_assigned.all().order_by('-modified_on')[:5]
        context['issue_sidebar_list'] = user.issues_assigned.all().order_by('-modified_on')[:5]
    else:
        context['project_sidebar_list'] = Project.objects.order_by('-visits')[:5]
        context['issue_sidebar_list'] = Issue.objects.order_by('-visits')[:5]
