from django import forms
from issues.models import Issue, Project

PRIORITY_CHOICES = [
    ('HIGH', 'High'),
    ('MED', 'Medium'),
    ('LOW', 'Low'),
]


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
        return project


class UpdateProjectForm(ProjectForm):

    def save(self, commit=True):
        project = super().save(commit=False)
        project.modified_by = self.user
        if commit:
            project.save()
        return project


class UpdateProjectForm2(forms.Form):

    title = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title',
            },
        ),
    )

    summary = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter a description',
            },
        ),
    )

    def __init__(self, user, *args, **kwargs):
        super(UpdateProjectForm, self).__init__(*args, **kwargs)
        self.user = user

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
                    'class': 'form-control',
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
        return issue


class UpdateIssueForm(IssueForm):

    def save(self, commit=True):
        issue = super().save(commit=False)
        issue.project = self.project
        issue.modified_by = self.user
        if commit:
            issue.save()
        return issue


class UpdateIssueForm2(forms.Form):

    title = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title',
            },
        ),
    )

    priority = forms.MultipleChoiceField(
        label='',
        widget=forms.RadioSelect(
            choices=PRIORITY_CHOICES,
            attrs={
                'class': 'form-control',
            },
        ),
    )

    summary = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter a description',
            },
        ),
    )
