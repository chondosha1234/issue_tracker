from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.urls import reverse
from django.contrib.auth import get_user_model
import time

from .base import FunctionalTest

User = get_user_model()

class TestUserCRUD(FunctionalTest):

    def test_user_create_update_and_delete_project_and_issue(self):

        # user logs in
        self.login_user_for_test()
        user = User.objects.get(email='user1234@example.org')

        # they go to their user page and see buttons to create new project
        self.browser.get(self.live_server_url + reverse('issues:user_home', args=[user.pk]))
        new_project_btn = self.wait_for_element_link('Create Project')

        # they click on create new project and are taken to a page with form
        new_project_btn.click()
        self.assertRegex(self.browser.current_url, '/create_project')
        title = self.wait_for_element_name('title')
        summary = self.wait_for_element_name('summary')
        submit_btn = self.wait_for_element_selector('.btn')

        # they enter information to make a new project and hit submit
        title.send_keys('Test Project')
        summary.send_keys('This is a test project')
        submit_btn.click()

        # they are returned to their user page and now see their project listed
        # on their profile
        time.sleep(1)
        self.assertRegex(self.browser.current_url, '/user_home')
        project_title_link = self.wait_for_element_link('Test Project')

        # they click on the project and are linked to their project detail page
        project_title_link.click()
        self.assertRegex(self.browser.current_url, '/project_details/1')

        # they see a button to add an issue to project (because they are the owner/creator)
        create_issue_btn = self.wait_for_element_link('Create Issue')

        # they click the button and are taken to a form to create issue
        create_issue_btn.click()

        # they enter info and hit submit
        title = self.wait_for_element_name('title')
        priority = self.wait_for_element_id('id_priority_2')
        summary = self.wait_for_element_name('summary')
        submit_btn = self.wait_for_element_selector('.btn')

        title.send_keys('Test Issue')
        summary.send_keys('This is a test issue')
        priority.click()
        submit_btn.click()

        # they are taken back to project detail page and can see their issue on the list
        time.sleep(1)
        self.assertRegex(self.browser.current_url, '/project_details/1')
        issue_link = self.wait_for_element_link('Test Issue')

        # they click on the issue and are taken to issue detail page
        issue_link.click()
        self.assertRegex(self.browser.current_url, '/issue_details/1')
        issue_title = self.wait_for_element_tag('h3').text
        self.assertIn('Test Issue', issue_title)

        # they see buttons for update and delete issue (because they created it)
        update_issue_btn = self.wait_for_element_link('Update Issue')
        delete_issue_btn = self.wait_for_element_id('delete-btn')

        # they click update and are taken to a page with form that is filled out with current
        # issue information
        update_issue_btn.click()
        self.assertRegex(self.browser.current_url, '/update_issue/1')
        title = self.wait_for_element_name('title')
        priority = self.wait_for_element_name('priority')
        summary = self.wait_for_element_name('summary')
        submit_btn = self.wait_for_element_selector('.btn')

        title_value = title.get_attribute('value')
        summary_value = summary.get_attribute('value')
        self.assertIn('Test Issue', title_value)
        self.assertIn('This is a test issue', summary_value)

        # they change title to "Changed test issue" and click submit
        title.send_keys('Changed Test Issue')
        submit_btn.click()

        # they are taken back to issue detail page and see the issue is altered
        self.assertRegex(self.browser.current_url, '/issue_details/1')
        issue_title = self.wait_for_element_tag('h3').text
        self.assertIn('Changed Test Issue', issue_title)

        # they click on delete issue and get a warning prompt
        delete_issue_btn = self.wait_for_element_id('delete-btn')
        delete_issue_btn.click()

        alert = self.browser.switch_to.alert
        self.assertIn('Are you sure you want to delete this issue?', alert.text)

        # they click no and nothing happens
        alert.dismiss()
        issue_title = self.wait_for_element_tag('h3').text
        self.assertIn('Changed Test Issue', issue_title)

        # they click delete again, and answer yes to prompt and they are redirected to
        # project details page and issue is gone
        delete_issue_btn = self.wait_for_element_id('delete-btn')
        delete_issue_btn.click()
        alert = self.browser.switch_to.alert
        self.assertIn('Are you sure you want to delete this issue?', alert.text)

        alert.accept()
        time.sleep(1)
        self.assertRegex(self.browser.current_url, '/project_details/1')
        with self.assertRaises(NoSuchElementException):
            self.wait_for_element_link('Changed Test Issue')

        # they return to project detail page and see button for delete project
        delete_project_btn = self.wait_for_element_id('delete-btn')

        # they click it and see similar warning and click yes
        delete_project_btn.click()
        alert = self.browser.switch_to.alert
        self.assertIn('Are you sure you want to delete this project?', alert.text)
        alert.accept()

        # they are redirected to user home page and there are no projects
        time.sleep(1)
        self.assertRegex(self.browser.current_url, '/user_home')
        with self.assertRaises(NoSuchElementException):
            self.wait_for_element_link('Test Project')

        # check if different user can't see buttons
