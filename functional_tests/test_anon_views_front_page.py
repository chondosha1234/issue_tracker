from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class AnonVisitsHomeTest(FucntionalTest):

    def test_visit_home_page_and_look_at_issues_and_projects(self):

        # user goes to the home page
        # they are not logged in

        # they see a navbar at the top with buttons 'home' 'issues' 'projects'

        # in the middle of the page they see a list of most views issues

        # they click on the top issue and it takes them to issue detail page

        # they see details about issue description, related project, users involved

        # they click on the project name and it takes them to a project detail page

        # project detail has some information at top and a list of issues related
        # to this project

        # user clicks projects button on navbar and is taken to list of proejcts
        # organized by most recent

        # user clicks issues on navbar and is taken to list of all issues organized
        # by most recent

        # user clicks home and is taken to issue list of most viewed

        # user clicks on top issue and sees button to edit issue

        # user clicks it and is redirected to log in page
