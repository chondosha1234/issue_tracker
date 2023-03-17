from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth import get_user_model
from .base import FunctionalTest
from issues.models import Project, Issue
import time

User = get_user_model()

class OpenAndCloseIssueTest(FunctionalTest):
    reset_sequences = True

    def test_open_and_close_issue(self):

        # user logs in
        self.login_user_for_test()

        # creating project and issue for testing
        self.create_project_and_issue_for_test()
        # after creating issue user is on project details page

        # user goes to issue_details page for the issue
        self.wait_for_element_link('Test Issue').click()

        # they see the issue is 'Open'
        issue_info = self.wait_for_element_class('item-info').text
        self.assertIn('Open', issue_info)

        # they see button to close issue and press it
        self.wait_for_element_class('dropdown-toggle').click()
        close_btn = self.wait_for_element_id('close-btn')
        close_btn.click()

        # now the issue is closed
        issue_info = self.wait_for_element_class('item-info').text
        self.assertIn('Closed', issue_info)

        # they see button to open issue and press it
        self.wait_for_element_class('dropdown-toggle').click()
        open_btn = self.wait_for_element_id('open-btn')
        open_btn.click()

        # now issue is open
        issue_info = self.wait_for_element_class('item-info').text
        self.assertIn('Open', issue_info)

        # they press open again while issue is open and nothing happens
        self.wait_for_element_class('dropdown-toggle').click()
        open_btn = self.wait_for_element_id('open-btn')
        open_btn.click()
        issue_info = self.wait_for_element_class('item-info').text
        self.assertIn('Open', issue_info)
