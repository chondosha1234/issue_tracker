from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
import time

from .base import FunctionalTest

class AddAndDeleteCommentsTest(FunctionalTest):
    reset_sequences = True

    def test_add_and_delete_comments_and_replies(self):

        # user logs in
        self.login_user_for_test()

        # creating project and issue to comment on
        self.create_project_and_issue_for_test()
        #after creating issue, user is on details page

        # user clicks on issue link and see issue details and text box at the bottom that
        # says 'comment'
        self.wait_for_element_link('Test Issue').click()
        comment_box = self.wait_for_element_name('text')
        submit_btn = self.wait_for_element_id('comment-btn')

        # user enters 'This is a great issue!' in the comment box and clicks submit
        comment_box.send_keys('This is a great issue')
        submit_btn.click()

        # the page refreshes and now there is the comment box and their comment appears below it
        self.assertRegex(self.browser.current_url, '/issue_details/')
        self.wait_for_element_name('text')
        comments = self.wait_for_element_class('comment-list').text
        self.assertIn('This is a great issue', comments)

        # on their comment they see a link that says 'reply'
        reply_link = self.wait_for_element_link('Reply')

        # they click it an another small text box appears below their comment
        reply_link.click()
        reply_box = self.browser.find_elements(By.NAME, 'text')[2] # there is first comment then first edit
        submit_btn = self.browser.find_elements(By.ID, 'comment-btn')[1]

        # they enter 'This is a great comment' and click submit
        reply_box.send_keys('This is a great comment')
        submit_btn.click()

        # the page refreshes again and now they can see their comment and their reply
        # under it (indented 1 layer)
        self.assertRegex(self.browser.current_url, '/issue_details/')
        comments = self.wait_for_element_class('comment-list').text
        self.assertIn('This is a great issue', comments)
        self.assertIn('This is a great comment', comments)

        # they see the reply has a reply button and does the same again, typing 'This is a great reply'
        reply_link = self.browser.find_elements(By.LINK_TEXT, 'Reply')[1]
        reply_link.click()
        reply_box = self.browser.find_elements(By.NAME, 'text')[4]
        submit_btn = self.browser.find_elements(By.ID, 'comment-btn')[2]

        reply_box.send_keys('This is a great reply')
        submit_btn.click()

        # the page refreshes and now there is the comment and the reply and next level of reply
        self.assertRegex(self.browser.current_url, '/issue_details/')
        comments = self.wait_for_element_class('comment-list').text
        self.assertIn('This is a great issue', comments)
        self.assertIn('This is a great comment', comments)
        self.assertIn('This is a great reply', comments)

        # they see each comment has an edit button
        # they press edit and the comment becomes a text box where the user can change the text
        # they change the first reply to 'This is a great comment but mine is better' and hit enter
        edit_link = self.browser.find_elements(By.LINK_TEXT, 'Edit')[1]
        edit_link.click()
        edit_link.click()
        edit_box = self.browser.find_elements(By.NAME, 'text')[3]
        edit_btn = self.browser.find_elements(By.ID, 'edit-btn')[1]
        edit_box.send_keys(' but mine is better')
        edit_btn.click()

        # the page refreshes and now the comment is changed
        self.assertRegex(self.browser.current_url, '/issue_details/')
        comments = self.wait_for_element_class('comment-list').text
        self.assertIn('This is a great issue', comments)
        self.assertIn('This is a great comment but mine is better', comments)
        self.assertIn('This is a great reply', comments)

        # they see there is also a delete button by each comment
        # they click delete on the last reply and an alert box appears asking to confirm deletion
        delete_btn = self.wait_for_element_id('delete-link-3').click()
        alert = self.browser.switch_to.alert
        self.assertIn('Are you sure you want to delete this comment?', alert.text)

        # they click yes and the reply is gone
        alert.accept()
        time.sleep(3)
        self.assertRegex(self.browser.current_url, '/issue_details/')
        comments = self.wait_for_element_class('comment-list').text
        self.assertIn('This is a great issue', comments)
        self.assertIn('This is a great comment but mine is better', comments)
        self.assertNotIn('This is a great reply', comments)

        # they then do the same to delete the top level comment and press yes to confirm
        delete_btn = self.wait_for_element_id('delete-link-1').click()
        alert = self.browser.switch_to.alert
        self.assertIn('Are you sure you want to delete this comment?', alert.text)
        alert.accept()
        time.sleep(3)

        # the top level comment and its reply are gone
        self.assertRegex(self.browser.current_url, '/issue_details/')
        comments = self.wait_for_element_class('comment-list').text
        self.assertNotIn('This is a great issue', comments)
        self.assertNotIn('This is a great comment but mine is better', comments)
        self.assertNotIn('This is a great reply', comments)
