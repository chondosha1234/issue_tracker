from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from .base import FunctionalTest
import time

class LoginTest(FunctionalTest):

    def test_can_login_and_logout(self):

        # User goes to home page and see on the top right corner a link / button
        # that says Log In
        # They press the button and it takes them to a login page
        self.browser.get(self.live_server_url + reverse('issues:home'))
        self.wait_for_element_class('navbar-toggler').click()
        self.browser.find_element(By.LINK_TEXT, 'Login').click()

        # user sees the url has the word login
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/login')

        # There is a field for username/email and password
        email = self.browser.find_element(By.NAME, 'email')
        password = self.browser.find_element(By.NAME, 'password')
        self.assertEqual(
            email.get_attribute('placeholder'),
            'Email Address'
        )

        # under the fields there is a link to create new account
        # user clicks link for create new account
        # new page has url with create_account in it
        self.browser.find_element(By.LINK_TEXT, 'Create New Account').click()
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/create_account')

        # the page is now for entering new account name and 2 password fields
        self.browser.find_element(By.NAME, 'email')
        self.browser.find_element(By.NAME, 'password')
        self.browser.find_element(By.NAME, 'confirm_password')

        # user sees link under the fields for 'Login' which takes them back to
        # the main login page
        # user clicks link for login and goes back to main login page.
        self.browser.find_element(By.LINK_TEXT, 'Login').click()
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/login')

        # User returns to create new account and enters information
        self.browser.find_element(By.LINK_TEXT, 'Create New Account').click()
        current_page_url = self.browser.current_url
        self.assertRegex(current_page_url, '/accounts/create_account')

        email = self.browser.find_element(By.NAME, 'email')
        password = self.browser.find_element(By.NAME, 'password')
        confirm_pwd = self.browser.find_element(By.NAME, 'confirm_password')
        submit = self.browser.find_element(By.CSS_SELECTOR, '.btn')

        email.send_keys("user1234@example.org")
        password.send_keys("chondosha5563")
        confirm_pwd.send_keys("chondosha5563")
        submit.click()

        # User presses submit button and is redirected to Login page
        if self.staging_server:
            self.browser.get(self.live_server_url + reverse('login'))
        else:
            time.sleep(2)  # need to wait
            current_page_url = self.browser.current_url
            self.assertRegex(current_page_url, '/accounts/login')

        # user enters new login information and is taken to home page
        email = self.browser.find_element(By.NAME, 'email')
        password = self.browser.find_element(By.NAME, 'password')
        submit = self.browser.find_element(By.CSS_SELECTOR, '.btn')

        email.send_keys("user1234@example.org")
        password.send_keys("chondosha5563")
        submit.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('issues:issue_list'))

        # user can now see in the top right corner that they are logged in
        # there is now a 'log out' link / button instead of log in
        self.wait_for_element_class('navbar-toggler').click()
        logout = self.browser.find_element(By.LINK_TEXT, 'Log out')

        # user clicks log out and is redirected to home page
        # where they see 'log in' link again
        logout.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('issues:issue_list'))
        self.wait_for_element_class('navbar-toggler').click()
        self.browser.find_element(By.LINK_TEXT, 'Login')
