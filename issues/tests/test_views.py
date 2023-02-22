from django.test import TestCase
from django.urls import resolve
from django.contrib.auth import get_user_model

from issues.views import home_page, IssueListView
from issues.models import Issue, Project

User = get_user_model()


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns(self):
        response = self.client.get('/')
        self.assertEquals(response.templates[0].name, 'issue_list.html')
        self.assertTemplateUsed(response, 'issue_list.html')


class IssueListTest(TestCase):

    def create_test_project(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = Project.objects.create(
            title="Test Project",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        return project

    def test_view_renders_issue_list_template(self):
        response = self.client.get('/issue_list')
        self.assertEquals(response.templates[0].name, 'issue_list.html')
        self.assertTemplateUsed(response, 'issue_list.html')

    def test_list_recent_shows_most_recent_issue_first(self):
        project = self.create_test_project()
        user = User.objects.get(email="user1234@example.org")
        old_issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
            visits=0
        )
        new_issue = Issue.objects.create(
            title="Test2",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
            visits=0
        )
        response = self.client.get("/issue_list/recent")
        self.assertEquals(response.context['issue_list'][0], new_issue)

    def test_list_popular_shows_most_visited_first(self):
        project = self.create_test_project()
        user = User.objects.get(email="user1234@example.org")
        issue1 = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
            visits=0
        )
        issue2 = Issue.objects.create(
            title="Test2",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
            visits=1
        )
        response = self.client.get("/issue_list/popular")
        self.assertEquals(response.context['issue_list'][0], issue2)

    def test_list_open_only_shows_open_issues(self):
        project = self.create_test_project()
        user = User.objects.get(email="user1234@example.org")
        issue1 = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            issue_status='Closed',
            created_by=user,
            modified_by=user,
            visits=0
        )
        issue2 = Issue.objects.create(
            title="Test2",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
            visits=0
        )
        response = self.client.get("/issue_list/open")
        self.assertEquals(Issue.objects.count(), 2)
        self.assertEquals(response.context['issue_list'].count(), 1)
        self.assertEquals(response.context['issue_list'][0], issue2)

    def test_list_closed_only_shows_closed_issues(self):
        project = self.create_test_project()
        user = User.objects.get(email="user1234@example.org")
        issue1 = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            issue_status='Closed',
            created_by=user,
            modified_by=user,
            visits=0
        )
        issue2 = Issue.objects.create(
            title="Test2",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
            visits=0
        )
        response = self.client.get("/issue_list/closed")
        self.assertEquals(Issue.objects.count(), 2)
        self.assertEquals(response.context['issue_list'].count(), 1)
        self.assertEquals(response.context['issue_list'][0], issue1)
