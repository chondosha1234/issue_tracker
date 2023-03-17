from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.urls import reverse
from django.contrib.auth import get_user_model
import time

from .base import FunctionalTest
from issues.models import Project, Issue

User = get_user_model()

class PaginationTest(FunctionalTest):

    def test_project_and_issue_lists_have_pagination(self):
        reset_sequences = True

        # creating many projects and issues to test pagination
        user = User.objects.create(name="chondosha", email="user1234@example.org", password="chondosha5563")
        for i in range(1, 51):
            Project.objects.create(
                title='project ' + str(i),
                summary="project",
                created_by=user,
                modified_by=user
            )

        project = Project.objects.get(id=1)
        for i in range(1, 51):
            Issue.objects.create(
                title='issue ' + str(i),
                project=project,
                summary="issue",
                created_by=user,
                modified_by=user,
            )

        # anon user goes to navvbar and clicks on projects
        self.browser.get(self.live_server_url + reverse('issues:home'))
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Projects').click()

        # they see there are 10 projects listed on the page with names '41' through '50'
        self.wait_for_element_link('project 41')
        self.wait_for_element_link('project 50')

        # at the bottom they see page select
        # it says 'Page 1' and it has numbers listed after which are links to other pages
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 1')

        # user clicks on the number '2' and is taken to another page starting with issue '31'
        self.wait_for_element_link('2').click()
        self.wait_for_element_link('project 31')
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 2')

        # they click the single right arrow and it moves them to page 3
        self.wait_for_element_link('next \u203A').click()
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 3')

        # the list has project '25' on this page
        self.wait_for_element_link('project 25')

        # they hit the double arrow and are on last page number 5
        self.wait_for_element_link('last \u00BB').click()
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 5')

        # they see there is project '5' on it
        self.wait_for_element_link('project 5')

        # they now click the double left arrow and return to page 1
        self.wait_for_element_link('\u00AB first').click()
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 1')

        # they click on project '1'
        self.wait_for_element_link('project 1').click()

        # on project details they see there are 10 issues listed on the page with names '41' through '50'
        self.assertRegex(self.browser.current_url, '/project_details/')
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 1')
        self.wait_for_element_link('issue 41')
        self.wait_for_element_link('issue 48')

        # they again click the right arrow and go to page 2 for this projects list of issues
        # and see issue '32' on the page
        self.wait_for_element_link('next \u203A').click()
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 2')
        self.wait_for_element_link('issue 32')

        # they hit double right arrow and see page 5 with issue '3'
        self.wait_for_element_link('last \u00BB').click()
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 5')
        self.wait_for_element_link('issue 3')

        # they go to navbar and hit issue tab there
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Issues').click()

        # they see list of issues with pagination at bottom again
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 1')

        # on page 1 there are no left arrows
        with self.assertRaises(NoSuchElementException):
            time.sleep(1)
            self.browser.find_element(By.LINK_TEXT, '\u00AB first')

        # they go to page 5 and there are no right arrows
        self.wait_for_element_link('last \u00BB').click()
        page = self.wait_for_element_class('current-page').text
        self.assertEqual(page, 'Page 5')

        with self.assertRaises(NoSuchElementException):
            time.sleep(1)
            self.browser.find_element(By.CLASS_NAME, 'last \u00BB')
