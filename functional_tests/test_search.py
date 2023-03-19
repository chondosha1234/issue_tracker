from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth import get_user_model
import time

from .base import FunctionalTest
from issues.models import Project, Issue

User = get_user_model()

class SearchBarTest(FunctionalTest):

    def test_search_projects_issues_and_users(self):

        # creating projects and issue for tests
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project = Project.objects.create(
            title="Test Project",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        other_project = Project.objects.create(
            title="Other Project",
            summary="This is a test project",
            created_by=user,
            modified_by=user
        )
        issue = Issue.objects.create(
            title="Test Issue",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )
        other_issue = Issue.objects.create(
            title="Other Issue",
            project=project,
            summary="This is a test issue",
            created_by=user,
            modified_by=user,
        )

        # any user (logged in or not) goes to home page and sees list of popular issues
        self.browser.get(self.live_server_url + reverse('issues:home'))

        # first they click on navbar menu and choose projects and are taken to list of projects
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Projects').click()

        # they see 2 projects there; 'Test Project' and 'Other Project'
        self.wait_for_element_link('Test Project')
        self.wait_for_element_link('Other Project')

        # at the top between navbar and main page they see a search bar
        search_input = self.wait_for_element_class('form-control')
        submit_btn = self.wait_for_element_class('search-btn')

        # they enter in a term to search  'Test Project'
        search_input.send_keys('Test Project')
        submit_btn.click()

        # a project comes up that says 'Test Project' but the project that says 'Other Project'
        # is not shown
        self.wait_for_element_link('Test Project')

        item_list = self.wait_for_element_class('list-group').text
        self.assertNotIn('Other Project', item_list)

        # they go to navbar and click on issues and see list with 2 issues; 'Test Issue' and
        # 'Other Issue'
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Issues').click()
        self.wait_for_element_link('Test Issue')
        self.wait_for_element_link('Other Issue')

        # again they type in the search bar 'Test Issue' and only that issue is shown
        search_input = self.wait_for_element_class('form-control')
        search_input.send_keys('Test Issue')
        self.wait_for_element_class('search-btn').click()

        self.wait_for_element_link('Test Issue')

        item_list = self.wait_for_element_class('list-group').text
        self.assertNotIn('Other Issue', item_list)

        # next the enter just 'Test' in the search and see both 'Test Project' and 'Test Issue'
        search_input = self.wait_for_element_class('form-control')
        search_input.clear()
        search_input.send_keys('Test')
        self.wait_for_element_class('search-btn').click()

        self.wait_for_element_link('Test Issue')

        item_list = self.wait_for_element_class('list-group').text
        self.assertNotIn('Other Project', item_list)

        # they enter user name and see a list of users with just the name.
        search_input = self.wait_for_element_class('form-control')
        search_input.clear()
        search_input.send_keys('chondosha')
        self.wait_for_element_class('search-btn').click()

        self.wait_for_element_link('chondosha')

        item_list = self.wait_for_element_class('list-group').text
        self.assertNotIn('Test Project', item_list)
