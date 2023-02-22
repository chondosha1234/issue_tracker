from django.test import TestCase
from django.urls import resolve
from issues.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns(self):
        response = self.client.get('/')
        self.assertEquals(response.templates[0].name, 'issue_list.html')
        self.assertTemplateUsed(response, 'issue_list.html')


class IssueListTest(TestCase):

    pass 
