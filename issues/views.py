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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    paginate_by = 49

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
