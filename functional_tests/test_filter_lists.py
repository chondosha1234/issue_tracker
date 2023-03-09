from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.urls import reverse
from django.contrib.auth import get_user_model
import time

from .base import FunctionalTest
from issues.models import Project, Issue

User = get_user_model()

class FilterTest(FunctionalTest):

    def test_filter_terms_sort_and_show_issues_and_projects(self):

        # creating projects and issues for testing purposes
        user = User.objects.create(name='chondosha', email="user1234@example.org", password="chondosha5563")
        project1 = Project.objects.create(
            title="Project one",
            summary="This is a test project",
            created_by=user,
            modified_by=user,
            visits=1
        )
        issue1 = Issue.objects.create(
            title="Issue one",
            project=project1,
            summary="This is a test issue",
            issue_status="Open",
            created_by=user,
            modified_by=user,
            visits=1
        )
        project2 = Project.objects.create(
            title="Project two",
            summary="This is a test project",
            created_by=user,
            modified_by=user,
            visits=0
        )
        issue2 = Issue.objects.create(
            title="Issue two",
            project=project2,
            summary="This is a test issue",
            issue_status="Closed",
            created_by=user,
            modified_by=user,
            visits=0
        )

        # any user (logged in or not) goes to issue list front page
        self.browser.get(self.live_server_url + reverse('issues:home'))

        # they click on navbar and select projects
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Projects').click()

        # they see a list of projects organized by popularity (visits)
        title = self.wait_for_element_tag('h2').text
        self.assertIn('Popular Projects', title)

        # they see project1 first and then project2
        project_list = self.wait_for_element_class('list-group')
        projects = project_list.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("Project one", projects[1].text)
        self.assertIn("Project two", projects[2].text)

        # They click the button that says 'Latest'
        self.wait_for_element_link('Latest').click()
        title = self.wait_for_element_tag('h2').text
        self.assertIn('Recent Projects', title)

        # now they see project2 first and then project1
        project_list = self.wait_for_element_class('list-group')
        projects = project_list.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("Project two", projects[1].text)
        self.assertIn("Project one", projects[2].text)

        # they click the button that says 'Most viewed'
        self.wait_for_element_link('Most Viewed').click()
        title = self.wait_for_element_tag('h2').text
        self.assertIn('Popular Projects', title)

        # now they see project1 first and then project2
        project_list = self.wait_for_element_class('list-group')
        projects = project_list.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("Project one", projects[1].text)
        self.assertIn("Project two", projects[2].text)

        # they click on navbar and click issues link
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Issues').click()

        # the issues are organized by popularity
        title = self.wait_for_element_tag('h2').text
        self.assertIn('Popular Issues', title)

        # issue1 is first and issue2 is second
        issue_list = self.wait_for_element_class('list-group')
        issues = issue_list.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("Issue one", issues[1].text)
        self.assertIn("Issue two", issues[2].text)

        # they click 'latest' and see issue2 and then issue1
        self.wait_for_element_link('Latest').click()
        title = self.wait_for_element_tag('h2').text
        self.assertIn('Recent Issues', title)

        issue_list = self.wait_for_element_class('list-group')
        issues = issue_list.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("Issue two", issues[1].text)
        self.assertIn("Issue one", issues[2].text)

        # they click 'most viewed' and see issue1 and then issue2
        self.wait_for_element_link('Most Viewed').click()

        issue_list = self.wait_for_element_class('list-group')
        issues = issue_list.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("Issue one", issues[1].text)
        self.assertIn("Issue two", issues[2].text)

        # next they click open to see only open issues which shows only issue1
        self.wait_for_element_link('Open').click()
        title = self.wait_for_element_tag('h2').text
        self.assertIn('Open Issues', title)

        issue_list = self.wait_for_element_class('list-group')
        issues = issue_list.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("Issue one", issues[1].text)
        self.assertEqual(len(issues), 2)

        # they click closed to see closed issues and see only issue2
        self.wait_for_element_link('Closed').click()
        title = self.wait_for_element_tag('h2').text
        self.assertIn('Closed Issues', title)

        issue_list = self.wait_for_element_class('list-group')
        issues = issue_list.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertIn("Issue two", issues[1].text)
        self.assertEqual(len(issues), 2)
