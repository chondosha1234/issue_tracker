from django.test import TestCase
from django.urls import resolve
from django.contrib.auth import get_user_model

from issues.views import home_page, IssueListView
from issues.models import Issue, Project
from issues.forms import (
    CreateProjectForm, CreateIssueForm,
    UpdateProjectForm, UpdateIssueForm
    )

User = get_user_model()


def create_test_project(user):
    project = Project.objects.create(
        title="Test Project",
        summary="This is a test project",
        created_by=user,
        modified_by=user
    )
    return project


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_without_user_redirects_to_issue_list(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/issue_list')

    def test_home_redirects_to_user_home_if_logged_in(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertRedirects(response, f'/user_home/{user.pk}')


class SearchTest(TestCase):

    def create_test_project(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = Project.objects.create(
            title='Test Project',
            summary='This is a test project',
            created_by=user,
            modified_by=user
        )
        return project

    def test_view_renders_search_template(self):
        response = self.client.get('/search', data={'search_query': 'Test'})
        self.assertEquals(response.templates[0].name, 'search.html')
        self.assertTemplateUsed(response, 'search.html')

    def test_search_returns_correct_project(self):
        project = self.create_test_project()
        response = self.client.get('/search', data={'search_query': 'Test Project'})
        self.assertEquals(response.context['results'][0], project)

    def test_search_returns_correct_issue(self):
         project = self.create_test_project()
         user = User.objects.get(email='user1234@example.org')
         issue = Issue.objects.create(
             title='Test Issue',
             project=project,
             summary='This is a test issue',
             created_by=user,
             modified_by=user,
         )
         response = self.client.get('/search', data={'search_query': 'Test Issue'})
         self.assertEquals(response.context['results'][0], issue)

    def test_search_returns_correct_user(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        response = self.client.get('/search', data={'search_query': 'user1234@example.org'})
        self.assertEquals(response.context['results'][0], user)

    def test_search_does_not_return_incorrect_issue(self):
        project = self.create_test_project()
        user = User.objects.get(email='user1234@example.org')
        issue = Issue.objects.create(
            title='Test Issue',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        other_issue = Issue.objects.create(
            title='Other Issue',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        response = self.client.get('/search', data={'search_query': 'Test Issue'})
        self.assertEquals(len(response.context['results']), 1)

    def test_search_does_not_return_incorrect_project(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = Project.objects.create(
            title='Test Project',
            summary='This is a test project',
            created_by=user,
            modified_by=user
        )
        other_project = Project.objects.create(
            title='Other Project',
            summary='This is a test project',
            created_by=user,
            modified_by=user
        )
        response = self.client.get('/search', data={'search_query': 'Test Project'})
        self.assertEquals(len(response.context['results']), 1)

    def test_search_does_not_return_incorrect_user(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        other_user = User.objects.create(name='other_guy', email='otheruser@example.org', password='chondosha5563')
        response = self.client.get('/search', data={'search_query': 'user1234@example.org'})
        self.assertEquals(len(response.context['results']), 1)

    def test_search_returns_both_issues_and_projects(self):
        project = self.create_test_project()
        user = User.objects.get(email='user1234@example.org')
        issue = Issue.objects.create(
            title='Test Project',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        response = self.client.get('/search', data={'search_query': 'Test Project'})
        self.assertEquals(len(response.context['results']), 2)
        self.assertEquals(response.context['results'][0], project)
        self.assertEquals(response.context['results'][1], issue)

    def test_partial_search_returns_results(self):
        project = self.create_test_project()
        response = self.client.get('/search', data={'search_query': 'Test'})
        self.assertEquals(response.context['results'][0], project)

    def test_partial_search_returns_issue_and_project(self):
        project = self.create_test_project()
        user = User.objects.get(email='user1234@example.org')
        issue = Issue.objects.create(
            title='Test Issue',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        response = self.client.get('/search', data={'search_query': 'Test'})
        self.assertEquals(len(response.context['results']), 2)
        self.assertEquals(response.context['results'][0], project)
        self.assertEquals(response.context['results'][1], issue)


class UserHomeTest(TestCase):

    def test_view_renders_user_home_template(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        self.client.force_login(user)
        response = self.client.get(f'/user_home/{user.pk}')
        self.assertEquals(response.templates[0].name, 'user_home.html')
        self.assertTemplateUsed(response, 'user_home.html')


class UserProfileTest(TestCase):
    pass


class UserListTest(TestCase):
    pass


class IssueListTest(TestCase):

    def create_test_project(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
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


class IssueDetailTest(TestCase):

    def test_view_renders_correct_template(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            issue_status='Open',
            created_by=user,
            modified_by=user,
        )
        response = self.client.get(f'/issue_details/{issue.id}')
        self.assertEquals(response.templates[0].name, 'issue_details.html')
        self.assertTemplateUsed(response, 'issue_details.html')


    def test_view_adds_visit_to_issue(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            issue_status='Open',
            created_by=user,
            modified_by=user,
        )
        self.assertEqual(issue.visits, 0)
        response = self.client.get(f'/issue_details/{issue.id}')
        changed_issue = Issue.objects.get(id=issue.id)
        self.assertEqual(changed_issue.visits, 1)


class ProjectListViewTest(TestCase):

    def test_view_renders_project_list_template(self):
        response = self.client.get('/project_list')
        self.assertEquals(response.templates[0].name, 'project_list.html')
        self.assertTemplateUsed(response, 'project_list.html')

    def test_default_list_shows_most_recent_projects_first(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
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
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
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
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
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
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
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

    def test_view_adds_visit_to_project(self):
        project = self.create_test_project()
        self.assertEqual(project.visits, 0)
        response = self.client.get(f'/project_details/{project.id}')
        changed_project = Project.objects.get(id=project.id)
        self.assertEqual(changed_project.visits, 1)


class CreateProjectTest(TestCase):

    def test_GET_create_project_renders_correct_template(self):
        self.client.force_login(
            User.objects.get_or_create(name='chondosha', email="user1234@example.org", password="chondosha5563")[0]
        )
        response = self.client.get('/create_project')
        self.assertEquals(response.templates[0].name, 'create_project.html')
        self.assertTemplateUsed(response, 'create_project.html')

    def test_POST_creates_new_project(self):
        self.client.force_login(
            User.objects.get_or_create(name='chondosha', email="user1234@example.org", password="chondosha5563")[0]
        )
        self.assertEquals(Project.objects.count(), 0)
        response = self.client.post('/create_project', data={
            'title': 'Test',
            'summary': 'This is a test'
        })
        self.assertEquals(Project.objects.count(), 1)

    def test_POST_redirects_to_user_home(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        self.client.force_login(user)
        response = self.client.post('/create_project', data={
            'title': 'Test',
            'summary': 'This is a test'
        })
        self.assertRedirects(response, f'/user_home/{user.pk}')


class UpdateProjectTest(TestCase):

    def test_create_project_renders_correct_template(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        response = self.client.get(f'/update_project/{project.id}')
        self.assertEquals(response.templates[0].name, 'update_project.html')
        self.assertTemplateUsed(response, 'update_project.html')

    def test_POST_updates_existing_project(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        self.assertEquals(Project.objects.count(), 1)
        self.assertEquals(project.title, 'Test Project')

        response = self.client.post(f'/update_project/{project.id}', data={
            'title': 'Test',
            'summary': 'This is a test'
        })
        self.assertEquals(Project.objects.count(), 1)
        updated_project = Project.objects.get(id=project.id)
        self.assertEquals(updated_project.title, 'Test')

    def test_POST_redirects_to_project_details(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        response = self.client.post(f'/update_project/{project.id}', data={
            'title': 'Test',
            'summary': 'This is a test'
        })
        self.assertRedirects(response, f'/project_details/{project.id}')


class DeleteProjectTest(TestCase):

    def test_succesful_POST_deletes_project(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        self.assertEquals(Project.objects.count(), 1)

        response = self.client.post(f'/delete_project/{project.id}')
        self.assertEquals(Project.objects.count(), 0)

    def test_successful_POST_redirects_to_user_home(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)

        response = self.client.post(f'/delete_project/{project.id}')
        self.assertRedirects(response, f'/user_home/{user.pk}')

    def test_other_user_cannot_delete_project(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        other_user = User.objects.create(email="other_user@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(other_user)
        self.assertEquals(Project.objects.count(), 1)

        response = self.client.post(f'/delete_project/{project.id}')
        self.assertEquals(Project.objects.count(), 1)

    def test_unsuccessful_POST_redirects_to_project_details(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        other_user = User.objects.create(email="other_user@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(other_user)

        response = self.client.post(f'/delete_project/{project.id}')
        self.assertRedirects(response, f'/project_details/{project.id}')


class AddAndRemoveUserToProjectTest(TestCase):

    def test_POST_redirects_to_project_details(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        response = self.client.post(f'/add_user_to_project/{project.id}', data={'username': 'chondosha'})
        self.assertRedirects(response, f'/project_details/{project.id}')

    def test_adds_user_to_list_of_assigned_users(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        self.assertEqual(project.assigned_users.count(), 0)

        response = self.client.post(f'/add_user_to_project/{project.id}', data={'username': 'chondosha'})
        self.assertEqual(project.assigned_users.count(), 1)

    def test_removes_user_from_list_of_assigned_users(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        project.assigned_users.add(user)
        project.save()
        self.assertEqual(project.assigned_users.count(), 1)

        response = self.client.post(f'/remove_user_from_project/{project.id}', data={'username': 'chondosha'})
        self.assertEqual(project.assigned_users.count(), 0)


class CreateIssueTest(TestCase):

    def test_GET_create_project_renders_correct_template(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        response = self.client.get(f'/create_issue/{project.id}')
        self.assertEquals(response.templates[0].name, 'create_issue.html')
        self.assertTemplateUsed(response, 'create_issue.html')

    def test_POST_creates_new_issue(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)
        self.assertEquals(Issue.objects.count(), 0)
        response = self.client.post(f'/create_issue/{project.id}', data={
            'title': 'Test',
            'priority': 'LOW',
            'summary': 'This is a test'
        })
        self.assertEquals(Issue.objects.count(), 1)

    def test_POST_redirects_to_project_details(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.client.force_login(user)

        response = self.client.post(f'/create_issue/{project.id}', data={
            'title': 'Test',
            'priority': 'LOW',
            'summary': 'This is a test'
        })
        self.assertRedirects(response, f'/project_details/{project.id}')


class UpdateIssueTest(TestCase):

    def test_create_project_renders_correct_template(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)
        response = self.client.get(f'/update_issue/{issue.id}')
        self.assertEquals(response.templates[0].name, 'update_issue.html')
        self.assertTemplateUsed(response, 'update_issue.html')

    def test_POST_changes_existing_issue(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = create_test_project(user)
        issue = Issue.objects.create(
            title='Test',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)
        self.assertEquals(Issue.objects.count(), 1)
        self.assertEquals(issue.title, 'Test')

        response = self.client.post(f'/update_issue/{issue.id}', data={
            'title': 'Test Issue',
            'priority': 'LOW',
            'summary': 'This is a test'
        })
        self.assertEquals(Issue.objects.count(), 1)
        updated_issue = Issue.objects.get(id=issue.id)
        self.assertEquals(updated_issue.title, 'Test Issue')

    def test_POST_redirects_to_issue_detail(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = create_test_project(user)
        issue = Issue.objects.create(
            title='Test',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)

        response = self.client.post(f'/update_issue/{issue.id}', data={
            'title': 'Test Issue',
            'priority': 'LOW',
            'summary': 'This is a test'
        })
        self.assertRedirects(response, f'/issue_details/{issue.id}')


class DeleteIssueTest(TestCase):

    def test_succesful_POST_deletes_issue(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)
        self.assertEquals(Issue.objects.count(), 1)

        response = self.client.post(f'/delete_issue/{issue.id}')
        self.assertEquals(Issue.objects.count(), 0)

    def test_successful_POST_redirects_to_project_details(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)

        response = self.client.post(f'/delete_issue/{issue.id}')
        self.assertRedirects(response, f'/project_details/{project.id}')

    def test_other_user_cannot_delete_issue(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        other_user = User.objects.create(name='other_guy', email="other_user@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(other_user)
        self.assertEquals(Issue.objects.count(), 1)

        response = self.client.post(f'/delete_issue/{issue.id}')
        self.assertEquals(Issue.objects.count(), 1)

    def test_unsuccessful_POST_redirects_to_issue_details(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        other_user = User.objects.create(name='other_guy', email="other_user@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(other_user)

        response = self.client.post(f'/delete_issue/{issue.id}')
        self.assertRedirects(response, f'/issue_details/{issue.id}')


class AddAndRemoveUserToIssueTest(TestCase):

    def test_POST_redirects_to_project_details(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)
        response = self.client.post(f'/add_user_to_issue/{issue.id}', data={'username': 'chondosha'})
        self.assertRedirects(response, f'/issue_details/{issue.id}')

    def test_adds_user_to_list_of_assigned_users(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)
        self.assertEqual(issue.assigned_users.count(), 0)

        response = self.client.post(f'/add_user_to_issue/{issue.id}', data={'username': 'chondosha'})
        self.assertEqual(issue.assigned_users.count(), 1)

    def test_removes_user_from_list_of_assigned_users(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)
        issue.assigned_users.add(user)
        issue.save()
        self.assertEqual(issue.assigned_users.count(), 1)

        response = self.client.post(f'/remove_user_from_issue/{issue.id}', data={'username': 'chondosha'})
        self.assertEqual(issue.assigned_users.count(), 0)


class OpenAndCloseIssueTest(TestCase):

    def test_open_view_redirects_to_issue_details(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = create_test_project(user)
        issue = Issue.objects.create(
            title='Test',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)

        response = self.client.post(f'/open_issue/{issue.id}')
        self.assertRedirects(response, f'/issue_details/{issue.id}')

    def test_POST_opens_a_closed_issue(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = create_test_project(user)
        issue = Issue.objects.create(
            title='Test',
            project=project,
            summary='This is a test issue',
            issue_status='Closed',
            created_by=user,
            modified_by=user,
        )
        issue.assigned_users.add(user)
        issue.save()
        self.client.force_login(user)

        response = self.client.post(f'/open_issue/{issue.id}')
        changed_issue = Issue.objects.get(id=issue.id)
        self.assertEqual(changed_issue.issue_status, 'Open')

    def test_POST_on_open_issue_does_nothing(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = create_test_project(user)
        issue = Issue.objects.create(
            title='Test',
            project=project,
            summary='This is a test issue',
            issue_status='Open',
            created_by=user,
            modified_by=user,
        )
        issue.assigned_users.add(user)
        issue.save()
        self.client.force_login(user)

        response = self.client.post(f'/open_issue/{issue.id}')
        changed_issue = Issue.objects.get(id=issue.id)
        self.assertEqual(changed_issue.issue_status, 'Open')

    def test_close_view_redirects_to_issue_details(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = create_test_project(user)
        issue = Issue.objects.create(
            title='Test',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        self.client.force_login(user)

        response = self.client.post(f'/close_issue/{issue.id}')
        self.assertRedirects(response, f'/issue_details/{issue.id}')

    def test_POST_closes_an_open_issue(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = create_test_project(user)
        issue = Issue.objects.create(
            title='Test',
            project=project,
            summary='This is a test issue',
            issue_status='Open',
            created_by=user,
            modified_by=user,
        )
        issue.assigned_users.add(user)
        issue.save()
        self.client.force_login(user)

        response = self.client.post(f'/close_issue/{issue.id}')
        changed_issue = Issue.objects.get(id=issue.id)
        self.assertEqual(changed_issue.issue_status, 'Closed')

    def test_POST_on_closed_issue_does_nothing(self):
        user = User.objects.create(name='chondosha', email='user1234@example.org', password='chondosha5563')
        project = create_test_project(user)
        issue = Issue.objects.create(
            title='Test',
            project=project,
            summary='This is a test issue',
            issue_status='Closed',
            created_by=user,
            modified_by=user,
        )
        issue.assigned_users.add(user)
        issue.save()
        self.client.force_login(user)

        response = self.client.post(f'/close_issue/{issue.id}')
        changed_issue = Issue.objects.get(id=issue.id)
        self.assertEqual(changed_issue.issue_status, 'Closed')
