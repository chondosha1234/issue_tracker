from django.test import TestCase
from django.contrib.auth import get_user_model

from issues.forms import CreateProjectForm, CreateIssueForm, UpdateProjectForm, UpdateIssueForm
from issues.models import Issue, Project

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


class UpdateProjectFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        form = UpdateProjectForm(user=user)
        self.assertIn('placeholder="Enter a title"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_changes_existing_project(self):
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


class UpdateIssueFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        user = User.objects.create(email="user1234@example.org", password="chondosha5563")
        project = create_test_project(user)
        form = CreateIssueForm(user=user, project=project)
        self.assertIn('placeholder="Enter a title"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_changes_existing_issue(self):
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
        updated_project = Issue.objects.get(pk=issue.id)
        self.assertEquals(updated_project.title, 'Test')
