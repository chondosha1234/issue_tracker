from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth import get_user_model

from .base import FunctionalTest

User = get_user_model()

class SideBarTest(FunctionalTest):

    def test_sidebar_displays_correct_info(self):
        reset_sequences = True

        # creating second user for test
        other_user = User.objects.create(name='other_guy', email="other_user@example.org", password="chondosha5563")
        other_user.set_password("chondosha5563")
        other_user.save()

        # user logs in and sees on their home page a side bar
        self.login_user_for_test()
        issues = self.wait_for_element_class('issue-items').text
        projects = self.wait_for_element_class('project-items').text

        # it says 'your recent issues' and 'your recent projects'
        # it says there are no issues or projects
        self.assertIn('Your recent issues:', issues)
        self.assertIn('There are currently no issues', issues)
        self.assertIn('Your recent projects:', projects)
        self.assertIn('There are currently no projects', projects)

        # user makes a project
        self.wait_for_element_link('Create Project').click()
        self.wait_for_element_name('title').send_keys('Test Project')
        self.wait_for_element_name('summary').send_keys('This is a test project')
        self.wait_for_element_selector('.btn').click()
        self.wait_for_element_link('Test Project').click()

        # now on the sidebar they see their project under the project tab
        issues = self.wait_for_element_class('issue-items').text
        projects = self.wait_for_element_class('project-items').text

        self.assertIn('There are currently no issues', issues)
        self.assertIn('Your recent projects:', projects)
        self.assertNotIn('There are currently no projects', projects)
        self.assertIn('Test Project', projects)

        # they first go to navbar and issues list so that the project will not be on main page
        # they click on link on sidebar to go to project details
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Issues').click()
        self.wait_for_element_link('Test Project').click()
        self.assertRegex(self.browser.current_url, '/project_details/')

        # they create an issue and see there is now an issue under their sidebar
        self.wait_for_element_class('dropdown-toggle').click()
        self.wait_for_element_link('Create Issue').click()
        self.wait_for_element_name('title').send_keys('Test Issue')
        self.wait_for_element_id('id_priority_2').click()
        self.wait_for_element_name('summary').send_keys('This is a test issue')
        self.wait_for_element_selector('.btn').click()

        issues = self.wait_for_element_class('issue-items').text
        projects = self.wait_for_element_class('project-items').text

        self.assertIn('Test Issue', issues)
        self.assertNotIn('There are currently no issues', issues)
        self.assertNotIn('There are currently no projects', projects)
        self.assertIn('Test Project', projects)

        # they log out and a different user logs in
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Log out').click()

        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Login').click()

        self.wait_for_element_name('name').send_keys('other_guy')
        self.wait_for_element_name('password').send_keys('chondosha5563')
        self.wait_for_element_selector('.btn').click()

        # they have no issues or projects under their sidebar
        issues = self.wait_for_element_class('issue-items').text
        projects = self.wait_for_element_class('project-items').text
        self.assertIn('Your recent issues:', issues)
        self.assertIn('There are currently no issues', issues)
        self.assertIn('Your recent projects:', projects)
        self.assertIn('There are currently no projects', projects)

        # they log out
        self.wait_for_element_class('navbar-toggler').click()
        self.wait_for_element_link('Log out').click()

        # anon user sees the issue and project on sidebar under 'Top issues' and 'Top Projects'
        self.browser.get(self.live_server_url + reverse('issues:home'))
        issues = self.wait_for_element_class('issue-items').text
        projects = self.wait_for_element_class('project-items').text
        self.assertIn('Top Issues:', issues)
        self.assertNotIn('There are currently no issues', issues)
        self.assertIn('Test Issue', issues)
        self.assertIn('Top Projects:', projects)
        self.assertNotIn('There are currently no projects', projects)
        self.assertIn('Test Project', projects)
