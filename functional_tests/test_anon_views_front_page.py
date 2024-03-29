from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth import get_user_model

from .base import FunctionalTest
from issues.models import Project, Issue

User = get_user_model()

class AnonVisitsHomeTest(FunctionalTest):
    reset_sequences = True

    def test_visit_home_page_and_look_at_issues_and_projects(self):

        # creating project and issues for testing purposes
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = Project.objects.create(
            title="Test Project",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        issue = Issue.objects.create(
            title="Test",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
            visits=0
        )

        # user goes to the home page
        # they are not logged in
        self.browser.get(self.live_server_url + reverse('issues:home'))
        self.assertIn('Issue Tracker', self.browser.title)
        self.assertRegex(self.browser.current_url, '/issue_list')

        # they see a navbar at the top with buttons 'home' 'issues' 'projects'
        navbar = self.wait_for_element_selector('.navbar')

        # in the middle of the page they see a list of most viewed issues
        title = self.wait_for_element_tag('h2').text
        self.assertIn('Popular Issues', title)
        self.wait_for_element_class('list-group-item')

        # they click on the top issue and it takes them to issue detail page
        issue_link = self.wait_for_element_link('Test')
        issue_link.click()
        self.assertRegex(self.browser.current_url, '/issue_details')

        # they see details about issue description, related project, users involved
        description = self.wait_for_element_class('issue-description').text
        self.assertIn('Test', description)
        self.assertIn('This is a test issue', description)
        self.assertIn('chondosha', description)

        # they click on the project name and it takes them to a project detail page
        project_link = self.wait_for_element_link('Test Project')
        project_link.click()
        self.assertRegex(self.browser.current_url, '/project_details')

        # project detail has some information at top and a list of issues related
        # to this project
        title = self.wait_for_element_tag('h4').text
        self.assertIn('Test Project', title)
        issue_list = self.wait_for_element_class('list-group').text
        self.assertIn('Test', issue_list)

        # user clicks projects button on navbar and is taken to list of proejcts
        # organized by most recent
        self.wait_for_element_class('navbar-toggler').click()
        project_btn = self.wait_for_element_link('Projects')
        project_btn.click()
        self.assertRegex(self.browser.current_url, '/project_list')
        project_list = self.wait_for_element_class('list-group').text
        self.assertIn('Test Project', project_list)

        # user clicks issues on navbar and is taken to list of all issues organized
        # by most recent
        self.wait_for_element_class('navbar-toggler').click()
        issues_btn = self.wait_for_element_link('Issues')
        issues_btn.click()
        issue_list = self.wait_for_element_class('list-group').text
        self.assertIn('Test', issue_list)

        # user clicks home and is taken to issue list of most viewed
