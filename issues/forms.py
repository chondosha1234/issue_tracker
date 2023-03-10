from django import forms
from django.contrib.auth import get_user_model

from issues.models import Issue, Project

User = get_user_model()

PRIORITY_CHOICES = [
    ('HIGH', {'label': 'High', 'class': 'form-check-input'}),
    ('MED', {'label': 'High', 'class': 'form-check-input'}),
    ('LOW', {'label': 'High', 'class': 'form-check-input'}),
]


class SearchForm(forms.Form):
    search_query = forms.CharField(
        label="",
        max_length=64,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search...',
            },
        ),
    )


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'summary']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a title',
                },
            ),
            'summary': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a description',
                },
            ),
        }

    def __init__(self, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['title'].label = ''
        self.fields['summary'].label = ''


class CreateProjectForm(ProjectForm):

    def save(self, commit=True):
        project = super().save(commit=False)
        project.created_by = self.user
        project.modified_by = self.user
        if commit:
            project.save()
        project.assigned_users.add(self.user)
        return project


class UpdateProjectForm(ProjectForm):

    def save(self, commit=True):
        project = super().save(commit=False)
        project.modified_by = self.user
        if commit:
            project.save()
        return project


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['title', 'priority', 'summary']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a title',
                },
            ),
            'priority': forms.RadioSelect(
                choices=PRIORITY_CHOICES,
                attrs={
                    'class': 'form-check',
                },
            ),
            'summary': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a description',
                },
            ),
        }

    def __init__(self, user, project, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.user = user
        self.project = project
        self.fields['title'].label = ''
        self.fields['priority'].label = ''
        self.fields['summary'].label = ''


class CreateIssueForm(IssueForm):

    def save(self, commit=True):
        issue = super().save(commit=False)
        issue.project = self.project
        issue.created_by = self.user
        issue.modified_by = self.user
        if commit:
            issue.save()
        issue.assigned_users.add(self.user)
        return issue


class UpdateIssueForm(IssueForm):

    def save(self, commit=True):
        issue = super().save(commit=False)
        issue.project = self.project
        issue.modified_by = self.user
        if commit:
            issue.save()
        return issue


class AddUserForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=64,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username',
            },
        ),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(name=username).exists():
            raise forms.ValidationError("This username does not exist")
        return username
