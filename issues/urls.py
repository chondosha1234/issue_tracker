from django.urls import path
from . import views

app_name="issues"

urlpatterns = [
    path('', views.home_page, name='home'),
    path('issue_list', views.IssueListView.as_view(), name='issue_list'),
    path('issue_list/<filter_term>', views.IssueListView.as_view(), name='issue_list'),
    path('issue_details/<issue_id>', views.IssueDetailView.as_view(), name='issue_details'),
    path('create_issue/<issue_id>', views.create_issue, name='create_issue'),
    path('edit_issue/<issue_id>', views.edit_issue, name='edit_issue'),
    path('delete_issue/<issue_id>', views.delete_issue, name='delete_issue'),
    path('project_list', views.ProjectListView.as_view(), name='project_list'),
    path('project_list/<filter_term>', views.ProjectListView.as_view(), name='project_list'),
    path('project_details/<project_id>', views.ProjectDetailView.as_view(), name='project_details'),
    path('project_details/<project_id>/<filter_term>', views.ProjectDetailView.as_view(), name='project_details'),
]
