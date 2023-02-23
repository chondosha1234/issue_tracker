from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_created_by')
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_modified_by')
    visits = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_on', 'title')

    def __str__(self):
        return self.title


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MED', 'Medium'),
        ('LOW', 'Low'),
    ]
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed')
    ]

    title = models.CharField(max_length=64)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    summary = models.TextField()  # maybe different text field
    issue_status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='Open')
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES, default='Low')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_created_by')
    modified_on = models.DateField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_modified_by')
    visits = models.IntegerField(default=0)

    class Meta:
        ordering = ('issue_status', 'priority', '-created_on', '-visits')
        #unique_together = ('project', 'title')

    def __str__(self):
        return self.title
