from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('issue_list', views.IssueListView.as_view(), name='issue_list'),
    path('issue_list/<filter_term>', views.IssueListView.as_view(), name='issue_list'),
]
