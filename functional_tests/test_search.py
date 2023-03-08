from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base import FunctionalTest

class SearchBarTest(FunctionalTest):

    def test_search_projects_issues_and_users(self):
        pass

        # any user (logged in or not) goes to home page and sees list of popular issues

        # first they click on navbar menu and choose projects and are taken to list of projects

        # they see 2 projects there; 'Test Project' and 'Other Project'

        # at the top between navbar and main page they see a search bar

        # they enter in a term to search  'Test Project'

        # a project comes up that says 'Test Project' but the project that says 'Other Project'
        # is not shown

        # they go to navbar and click on issues and see list with 2 issues; 'Test Issue' and
        # 'Other Issue'

        # again they type in the search bar 'Test Issue' and only that issue is shown

        # next they hit home button and just see popular issues

        # they enter 'Test Project' from this page and are shown just that project again

        # next the enter just 'Test' in the search and see both 'Test Project' and 'Test Issue'

        # they enter their user name and see a list of users with just their name.
