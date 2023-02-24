from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base import FunctionalTest

class TestUserCRUD(FunctionalTest):

    def test_user_create_update_and_delete_project_and_issue(self):

        # user logs in
        self.login_user_for_test()

        # they go to their user page and see buttons to create new project or issue

        # they click on create new project and are taken to a page with form

        # they enter information to make a new project and hit submit

        # they are returned to their user page and now see their project listed
        # on their profile

        # they click on the project and are linked to their project detail page

        # they see a button to add an issue to project (because they are the owner/creator)

        # they click the button and are taken to a form to create issue
        # they enter info and hit submit

        # they are taken back to project detail page and can see their issue on the list

        # they click on the issue and are taken to issue detail page

        # they see buttons for update and delete issue (because they created it)

        # they click update and are taken to a page with form that is filled out with current
        # issue information

        # they change description to "Changed test issue" and click submit

        # they are taken back to issue detail page and see the issue is altered

        # they click on delete issue and get a warning prompt

        # they click no and nothing happens
        # they click delete again, and answer yes to prompt and the issue is gone

        # they return to project detail page and see button for delete project

        # they click it and see similar warning and click yes

        # they are redirected to user home page and there are no projects
