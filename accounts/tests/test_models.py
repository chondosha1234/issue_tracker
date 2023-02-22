from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_has_email_and_password(self):
        user = User(email="user1234@example.org", password="password1234")
        user.full_clean() # should not raise
