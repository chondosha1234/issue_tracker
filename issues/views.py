from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from issues.models import Issue, Project


def home_page(request):
    return render(request, 'issue_list.html')


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
