from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('issue_list', views.IssueListView.as_view(), name='issue_list'),
    path('issue_list/<filter_term>', views.IssueListView.as_view(), name='issue_list'),
    path('project_list', views.ProjectListView.as_view(), name='project_list'),
    path('project_list/<filter_term>', views.ProjectListView.as_view(), name='project_list'),
    path('project_details/<project_id>', views.ProjectDetailView.as_view(), name='project_details'),
    path('project_details/<project_id>/<filter_term>', views.ProjectDetailView.as_view(), name='project_details'),
]
