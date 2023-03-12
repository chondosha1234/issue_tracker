from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.urls import reverse
from django.contrib.auth import get_user_model
import time

from .base import FunctionalTest
from issues.models import Project, Issue

User = get_user_model()

class AddAndRemoveUsersTest(FunctionalTest):
    reset_sequences = True

    def switch_user(self, new_user):
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Log out').click()

        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Login').click()

        self.wait_for_element_name('name').send_keys(new_user)
        self.wait_for_element_name('password').send_keys("chondosha5563")
        self.wait_for_element_selector('.btn').click()

    def test_add_and_remove_user_from_project_and_issue(self):

        # login user
        self.login_user_for_test()

        # creating project and issues for testing purposes
        self.create_project_and_issue_for_test()
        other_user = User.objects.create(name='other_guy', email="other_user@example.org", password="chondosha5563")
        other_user.set_password("chondosha5563")
        other_user.save()

        # user goes to home page and and sees their project
        self.browser.get(self.live_server_url + reverse('issues:home'))

        # they click on project
        self.wait_for_element_link('Test Project').click()

        # they see button to add user to project
        # they click button and an input pops up to enter username
        self.wait_for_element_link('Add User').click()
        input = self.wait_for_element_name('username')
        submit_btn = self.wait_for_element_id('add-user-btn')

        # they enter username and press submit
        input.send_keys('other_guy')
        submit_btn.click()

        # they click on issue and see button to add user to issue
        self.wait_for_element_link('Test Issue').click()

        # they click the button and an input pops up to enter a username
        self.wait_for_element_link('Add User').click()
        input = self.wait_for_element_name('username')
        submit_btn = self.wait_for_element_id('add-user-btn')

        # they enter username and press submit
        input.send_keys('other_guy')
        submit_btn.click()

        # user logs out and 'other_user' logs in
        self.switch_user('other_guy')

        # they see on their home page the project because they have been added
        # even though they didnt create it
        # they click on project and see buttons available
        self.wait_for_element_link('Test Project').click()

        self.wait_for_element_link('Update Project')
        self.wait_for_element_link('Create Issue')

        # they click on project and see buttons available
        self.wait_for_element_link('Test Issue').click()

        self.wait_for_element_link('Update Issue')

        # they log out and main user logs back in
        self.switch_user('chondosha')

        # they go to project and see remove user button
        self.wait_for_element_link('Test Project').click()

        # they enter the other_user name and press submit
        self.wait_for_element_link('Remove User').click()
        remove_input = self.browser.find_elements(By.NAME, 'username')[1]
        remove_input.send_keys('other_guy')
        #self.wait_for_element_name('username').send_keys('other_guy')
        self.wait_for_element_id('remove-user-btn').click()

        # they do the same with the issue and press submit
        self.wait_for_element_link('Test Issue').click()
        self.wait_for_element_link('Remove User').click()
        remove_input = self.browser.find_elements(By.NAME, 'username')[1]
        remove_input.send_keys('other_guy')
        #self.wait_for_element_name('username').send_keys('other_guy')
        self.wait_for_element_id('remove-user-btn').click()

        # user logs out and other_user logs in and no has no project on home page
        self.switch_user('other_guy')
        with self.assertRaises(NoSuchElementException):
            time.sleep(1)
            self.browser.find_element(By.LINK_TEXT, 'Test Project')

        # they go to projects list and see the project and click on it
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Projects').click()
        self.wait_for_element_link('Test Project').click()

        # they cannot see buttons because they are not assigned
        with self.assertRaises(NoSuchElementException):
            time.sleep(1)
            self.browser.find_element(By.LINK_TEXT, 'Update Project')

        # they click on issue and cannot see buttons here either
        self.wait_for_element_link('Test Issue').click()
        with self.assertRaises(NoSuchElementException):
            time.sleep(1)
            self.browser.find_element(By.LINK_TEXT, 'Update Issue')
