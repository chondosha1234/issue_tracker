from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base import FunctionalTest

class AddAndDeleteCommentsTest(FunctionalTest):
    reset_sequences = True

    def test_add_and_delete_comments_and_replies(self):

        # user logs in

        # creating project and issue to comment on

        #after creating issue, user is on details page

        # user clicks on issue link and see issue details and text box at the bottom that
        # says 'comment'

        # user enters 'This is a great issue!' in the comment box and clicks submit

        # the page refreshes and now there is the comment box and their comment appears below it

        # on their comment they see a link that says 'reply'

        # they click it an another small text box appears below their comment

        # they enter 'This is a great comment' and click submit

        # the page refreshes again and now they can see their comment and their reply
        # under it (indented 1 layer)

        # they see the reply has a reply button and does the same again, typing 'This is a great reply'

        # the page refreshes and now there is the comment and the reply and next level of reply

        # they see each comment has an edit button

        # they press edit and the comment becomes a text box where the user can change the text

        # they change the first reply to 'This is a reply to a great comment' and hit enter

        # the page refreshes and now the comment is changed

        # they see there is also a delete button by each comment

        # they click delete on the last reply and an alert box appears asking to confirm deletion

        # they click yes and the reply is gone

        # they then do the same to delete the top level comment and press yes to confirm

        # the top level comment and its reply are gone
