from django.test import TestCase
from django.contrib.auth import get_user_model

from issues.models import Issue, Project, Comment

User = get_user_model()

class ProjectModelTest(TestCase):

    def test_number_of_issues_property(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = Project.objects.create(
            title='Test Project',
            summary='This is a test project',
            created_by=user,
            modified_by=user
        )
        issue1 = Issue.objects.create(
            title='Test Issue 1',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        issue2 = Issue.objects.create(
            title='Test Issue 2',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        self.assertEqual(project.number_of_issues, 2)


class CommentModelTest(TestCase):

    def test_reply_count_returns_correct_number_replies(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = Project.objects.create(
            title='Test Project',
            summary='This is a test project',
            created_by=user,
            modified_by=user
        )
        issue = Issue.objects.create(
            title='Test Issue',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        comment1 = Comment.objects.create(
            user=user,
            text='This is a comment',
            issue=issue,
        )
        self.assertEqual(comment1.reply_count, 0)

        comment2 = Comment.objects.create(
            user=user,
            text='This is a comment',
            issue=issue,
            parent_comment=comment1,
        )
        self.assertEqual(comment1.reply_count, 1)

    def test_reply_count_recursively_counts_sub_comments(self):
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = Project.objects.create(
            title='Test Project',
            summary='This is a test project',
            created_by=user,
            modified_by=user
        )
        issue = Issue.objects.create(
            title='Test Issue',
            project=project,
            summary='This is a test issue',
            created_by=user,
            modified_by=user,
        )
        comment1 = Comment.objects.create(
            user=user,
            text='This is a comment',
            issue=issue,
        )
        self.assertEqual(comment1.reply_count, 0)

        comment2 = Comment.objects.create(
            user=user,
            text='This is a comment',
            issue=issue,
            parent_comment=comment1,
        )
        self.assertEqual(comment1.reply_count, 1)
        self.assertEqual(comment2.reply_count, 0)

        comment3 = Comment.objects.create(
            user=user,
            text='This is a comment',
            issue=issue,
            parent_comment=comment2,
        )

        self.assertEqual(comment1.reply_count, 2)
        self.assertEqual(comment2.reply_count, 1)
