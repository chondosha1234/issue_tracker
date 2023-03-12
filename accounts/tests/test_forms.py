from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.forms import LoginForm, CreateAccountForm

User = get_user_model()

class CreateAccountFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        form = CreateAccountForm()
        self.assertIn('placeholder="User Name"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_blank_username(self):
        form = CreateAccountForm(data={
            "name": "",
            "email": "user1234@example.org",
            "password": "chondosha5563",
            "confirm_password": "chondosha5563"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ["Must enter a username"])

    def test_form_validation_for_blank_email(self):
        form = CreateAccountForm(data={
            "name": "chondosha",
            "email": "",
            "password": "chondosha5563",
            "confirm_password": "chondosha5563"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ["Must enter an email"])

    def test_form_validation_for_no_password(self):
        form = CreateAccountForm(data={
            "name": "chondosha",
            "email": "user1234@example.org",
            "password": "",
            "confirm_password": ""})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_non_matching_passwords(self):
        form = CreateAccountForm(data={
            "name": "chondosha",
            "email": "user1234@example.org",
            "password": "chondosha5563",
            "confirm_password": "wrongpassword"})
        self.assertFalse(form.is_valid())

    def test_form_saves_user(self):
        form = CreateAccountForm(data={
            "name": "chondosha",
            "email": "user1234@example.org",
            "password": "chondosha5563",
            "confirm_password": "chondosha5563"})
        form.save()
        self.assertEqual(User.objects.count(), 1)


class LoginFormTest(TestCase):

    def test_form_input_has_placeholder_and_css_class(self):
        form = LoginForm()
        self.assertIn('placeholder="User Name"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_blank_username(self):
        form = LoginForm(data={'name': "", 'password': "chondosha5563"})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_no_password(self):
        form = LoginForm(data={'name': "chondosha", 'password': ""})
        self.assertFalse(form.is_valid())
