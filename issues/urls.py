from django.urls import path
from . import views

app_name="issues"

urlpatterns = [
    path('', views.home_page, name='home'),
    path('search', views.search, name='search'),
    path('issue_list', views.IssueListView.as_view(), name='issue_list'),
    path('issue_list/<filter_term>', views.IssueListView.as_view(), name='issue_list'),
    path('issue_details/<issue_id>', views.IssueDetailView.as_view(), name='issue_details'),
    path('create_issue/<project_id>', views.create_issue, name='create_issue'),
    path('update_issue/<issue_id>', views.update_issue, name='update_issue'),
    path('delete_issue/<issue_id>', views.delete_issue, name='delete_issue'),
    path('add_user_to_issue/<issue_id>', views.add_user_to_issue, name='add_user_to_issue'),
    path('remove_user_from_issue/<issue_id>', views.remove_user_from_issue, name='remove_user_from_issue'),
    path('open_issue/<issue_id>', views.open_issue, name='open_issue'),
    path('close_issue/<issue_id>', views.close_issue, name='close_issue'),
    path('project_list', views.ProjectListView.as_view(), name='project_list'),
    path('project_list/<filter_term>', views.ProjectListView.as_view(), name='project_list'),
    path('project_details/<project_id>', views.ProjectDetailView.as_view(), name='project_details'),
    path('project_details/<project_id>/<filter_term>', views.ProjectDetailView.as_view(), name='project_details'),
    path('create_project', views.create_project, name='create_project'),
    path('update_project/<project_id>', views.update_project, name='update_project'),
    path('delete_project/<project_id>', views.delete_project, name='delete_project'),
    path('add_user_to_project/<project_id>', views.add_user_to_project, name='add_user_to_project'),
    path('remove_user_from_project/<project_id>', views.remove_user_from_project, name='remove_user_from_project'),
    path('user_home/<user_id>', views.UserHome.as_view(), name='user_home'),
    path('user_profile/<user_id>', views.UserProfile.as_view(), name='user_profile')
]
