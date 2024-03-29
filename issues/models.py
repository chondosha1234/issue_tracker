from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_created_by')
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_modified_by')
    visits = models.IntegerField(default=0)
    assigned_users = models.ManyToManyField(User, related_name='projects_assigned')

    class Meta:
        ordering = ('-visits', '-created_on', 'title')

    def __str__(self):
        return self.title

    @property
    def issue_count(self):
        return self.issue_list.count()


class Issue(models.Model):
    PRIORITY_CHOICES = [
        (3, 'High'),
        (2, 'Medium'),
        (1, 'Low'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed')
    ]

    title = models.CharField(max_length=64)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issue_list')
    summary = models.TextField()
    issue_status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='Open')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_created_by')
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_modified_by')
    visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(auto_now=True)
    assigned_users = models.ManyToManyField(User, related_name='issues_assigned')
    closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='closed_issues', default=None, null=True, blank=True)

    class Meta:
        ordering = ('-visits', '-created_on', 'issue_status', 'priority')

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    depth = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    @property
    def reply_count(self):
        total = self.replies.count()
        for reply in self.replies.all():
            if reply:
                total += reply.reply_count
        return total
