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
        """
        filter_set = Issue.objects.all()
        if self.request.GET.get('recent'):
            filter_set = Issue.objects.order_by('-created_on')
        if self.request.GET.get('popular'):
            filter_set = Issue.objects.order_by('-visits')
        if self.request.GET.get('open'):
            filter_set = Issue.objects.filter(status='Open')
        if self.request.GET.get('closed'):
            filter_set = Issue.objects.filter(status='Closed')
        context['issues'] = filter_set
        """
        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    paginate_by = 49

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
