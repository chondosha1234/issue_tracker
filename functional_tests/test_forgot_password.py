from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.core import mail
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth import get_user_model
import re
import time

from .base import FunctionalTest

User = get_user_model()

class ForgotPasswordTest(FunctionalTest):

    @patch('django.core.mail.backends.smtp.EmailBackend.send_messages')
    def test_forgot_password(self, mock_send_messages):
        if self.staging_server:
            test_email = 'chonmailservice@gmail.com'
        else:
            test_email = 'test@example.org'

        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")

        # user goes to login page
        self.browser.get(self.live_server_url + reverse('login'))

        # they see forgot password link and click it.
        self.wait_for_element_link('Forgot Password?').click()

        # it takes them to a forgot password email request page
        self.assertRegex(self.browser.current_url, '/accounts/forgot-password')

        # they see a place to input their email and a button requesting instructions
        email_input = self.wait_for_element_id('id_email')
        submit_btn = self.wait_for_element_class('btn')

        # they enter their email, 'user1234@example.org' and press the button
        email_input.send_keys('user1234@example.org')
        submit_btn.click()

        # they are directed to a page confirming an email was sent
        self.assertRegex(self.browser.current_url, 'password-reset/done')

        # they go to 'open' their email and see theres a new email and who sent it
        email = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [user.email])
        self.assertIn('Password reset', email.subject)

        # they click on the link there which takes them to
        # a page to reset the password
        url_pattern = r'http://[^\s/]+/accounts/reset/[^\s/]+/[^\s/]+/'
        link = re.search(url_pattern, email.body)
        self.browser.get(link.group())

        # there are 2 inputs for resetting password
        password_input = self.wait_for_element_id('id_new_password1')
        confirm_password_input = self.wait_for_element_id('id_new_password2')
        submit_btn = self.wait_for_element_class('btn')

        # they enter new password 'chondosha420' in both boxes and press enter
        password_input.send_keys('chondosha420')
        confirm_password_input.send_keys('chondosha420')
        submit_btn.click()

        # they are directed to reset complete page
        self.assertRegex(self.browser.current_url, 'reset/done')
        link = self.wait_for_element_link('log in page')
        link.click()

        # they return to login page by pressing link to return
        self.assertRegex(self.browser.current_url, 'login')

        # they enter username and new password and log in
        username = self.wait_for_element_name('name').send_keys('chondosha')
        password = self.wait_for_element_name('password').send_keys('chondosha420')
        btn = self.wait_for_element_selector('.btn').click()

        self.assertRegex(self.browser.current_url, '/user_home')
