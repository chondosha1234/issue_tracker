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


class ProjectListViewTest(TestCase):

    def test_view_renders_project_list_template(self):
        response = self.client.get('/project_list')
        self.assertEquals(response.templates[0].name, 'project_list.html')
        self.assertTemplateUsed(response, 'project_list.html')

    def test_default_list_shows_most_recent_projects_first(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        old_project = Project.objects.create(
            title="Test Project",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        new_project = Project.objects.create(
            title="Test Project 2",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        response = self.client.get("/project_list")
        self.assertEquals(response.context['project_list'][0], new_project)

    def test_list_recent_shows_most_recent_project_first(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        old_project = Project.objects.create(
            title="Test Project",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        new_project = Project.objects.create(
            title="Test Project 2",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )

        response = self.client.get("/project_list/recent")
        self.assertEquals(response.context['project_list'][0], new_project)

    def test_list_popular_shows_most_visited_project_first(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        old_project = Project.objects.create(
            title="Test Project",
            summary="This is a test project",
            created_by=user,
            modified_by=user,
            visits=0
        )
        new_project = Project.objects.create(
            title="Test Project 2",
            summary="This is a test project",
            created_by=user,
            modified_by=user,
            visits=1
        )

        response = self.client.get("/project_list/popular")
        self.assertEquals(response.context['project_list'][0], new_project)


class ProjectDetailViewTest(TestCase):

    def create_test_project(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = Project.objects.create(
            title="Test Project",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        return project

    def test_view_renders_project_details_template(self):
        project = self.create_test_project()
        user = User.objects.get(email="user1234@example.org")
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        response = self.client.get(f'/project_details/{project.id}')
        self.assertEquals(response.templates[0].name, 'project_details.html')
        self.assertTemplateUsed(response, 'project_details.html')

    def test_project_details_only_has_issues_for_that_project(self):
        project1 = self.create_test_project()
        user = User.objects.get(email="user1234@example.org")
        project2 = Project.objects.create(
            title="Test Project 2",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        issue1 = Issue.objects.create(
            title="Test",
            project=project1,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        issue2 = Issue.objects.create(
            title="Test",
            project=project2,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )

        response = self.client.get(f'/project_details/{project1.id}')
        self.assertEquals(response.context['issue_list'].count(), 1)
        self.assertEquals(response.context['issue_list'][0], issue1)

    def test_project_details_filters_open_and_closed_issues(self):
        project = self.create_test_project()
        user = User.objects.get(email="user1234@example.org")
        issue1 = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        issue2 = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            issue_status='Closed',
            created_by=user,
            modified_by=user,
        )

        response = self.client.get(f'/project_details/{project.id}/open')
        self.assertEquals(response.context['issue_list'].count(), 1)
        self.assertEquals(response.context['issue_list'][0], issue1)

        response = self.client.get(f'/project_details/{project.id}/closed')
        self.assertEquals(response.context['issue_list'].count(), 1)
        self.assertEquals(response.context['issue_list'][0], issue2)
