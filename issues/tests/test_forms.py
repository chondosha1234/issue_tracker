from django.test import TestCase
from django.contrib.auth import get_user_model

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


class CreateProjectFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        form = CreateProjectForm(user=user)
        self.assertIn('placeholder="Enter a title"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_blank_title(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        form = CreateProjectForm(user=user, data={
            'title': '',
            'summary': 'Test project'
        })
        self.assertFalse(form.is_valid())

    def test_form_validation_for_blank_summary(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        form = CreateProjectForm(user=user, data={
            'title': 'Test',
            'summary': ''
        })
        self.assertFalse(form.is_valid())

    def test_form_creates_and_saves_new_project(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        form = CreateProjectForm(user=user, data={
            'title': 'Test',
            'summary': 'Test project'
        })
        form.save()
        self.assertEquals(Project.objects.count(), 1)

    def test_create_adds_user_to_list_of_assigned_users(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        form = CreateProjectForm(user=user, data={
            'title': 'Test',
            'summary': 'Test project'
        })
        form.save()
        project = Project.objects.get(title='Test')
        self.assertEqual(project.assigned_users.count(), 1)
        self.assertEqual(project.assigned_users.first(), user)


class UpdateProjectFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        form = UpdateProjectForm(user=user)
        self.assertIn('placeholder="Enter a title"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_update_form_changes_existing_project(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.assertEquals(project.title, 'Test Project')
        form = UpdateProjectForm(user=user, instance=project, data={
            'title': 'Test',
            'summary': 'Test project'
        })
        form.save()
        self.assertEquals(Project.objects.count(), 1)
        updated_project = Project.objects.get(pk=project.id)
        self.assertEquals(updated_project.title, 'Test')

    def test_other_user_changes_modified_but_not_original_creator(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        self.assertEquals(project.created_by, user)
        self.assertEquals(project.modified_by, user)

        other_user = User.objects.create(email="other_user@example.org", password="chondosha5563")
        form = UpdateProjectForm(user=other_user, instance=project, data={
            'title': 'Test',
            'summary': 'Test project'
        })
        form.save()
        updated_project = Project.objects.get(pk=project.id)
        self.assertEquals(project.created_by, user)
        self.assertEquals(project.modified_by, other_user)


class CreateIssueFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        form = CreateIssueForm(user=user, project=project)
        self.assertIn('placeholder="Enter a title"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_blank_title(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        form = CreateIssueForm(user=user, project=project, data={
            'title': '',
            'priority': 'LOW',
            'summary': 'Test project'
        })
        self.assertFalse(form.is_valid())

    def test_form_validation_for_blank_summary(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        form = CreateIssueForm(user=user, project=project, data={
            'title': 'Test',
            'priority': 'LOW',
            'summary': ''
        })
        self.assertFalse(form.is_valid())

    def test_form_creates_and_saves_new_project(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        form = CreateIssueForm(user=user, project=project, data={
            'title': 'Test',
            'priority': 'LOW',
            'summary': 'Test project'
        })
        form.save()
        self.assertEquals(Issue.objects.count(), 1)

    def test_create_adds_user_to_list_of_assigned_users(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        form = CreateIssueForm(user=user, project=project, data={
            'title': 'Test',
            'priority': 'LOW',
            'summary': 'Test project'
        })
        form.save()
        issue = Issue.objects.get(title='Test')
        self.assertEqual(issue.assigned_users.count(), 1)
        self.assertEqual(issue.assigned_users.first(), user)


class UpdateIssueFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        form = CreateIssueForm(user=user, project=project)
        self.assertIn('placeholder="Enter a title"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_update_form_changes_existing_issue(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test Issue",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.assertEquals(issue.title, 'Test Issue')
        form = UpdateIssueForm(user=user, project=project, instance=issue, data={
            'title': 'Test',
            'priority': 'LOW',
            'summary': 'Test project'
        })
        form.save()
        self.assertEquals(Issue.objects.count(), 1)
        updated_issue = Issue.objects.get(pk=issue.id)
        self.assertEquals(updated_issue.title, 'Test')

    def test_update_form_changes_priority(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test Issue",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.assertEquals(issue.priority, 'Low')
        form = UpdateIssueForm(user=user, project=project, instance=issue, data={
            'title': 'Test',
            'priority': 'HIGH',
            'summary': 'Test project'
        })
        form.save()
        updated_issue = Issue.objects.get(pk=issue.id)
        self.assertEquals(updated_issue.priority, 'HIGH')

    def test_update_changes_modified_but_not_original_creator(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        issue = Issue.objects.create(
            title="Test Issue",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        self.assertEquals(issue.created_by, user)
        self.assertEquals(issue.modified_by, user)

        other_user = User.objects.create(email="other_user@example.org", password="chondosha5563")
        form = UpdateIssueForm(user=other_user, project=project, instance=issue, data={
            'title': 'Test',
            'priority': 'LOW',
            'summary': 'Test project'
        })
        form.save()
        updated_issue = Issue.objects.get(pk=issue.id)
        self.assertEquals(issue.created_by, user)
        self.assertEquals(issue.modified_by, other_user)
