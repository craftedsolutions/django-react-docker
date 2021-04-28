import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_todays_date(self):
        time = timezone.now()
        today_question = Question(pub_date=time)

        self.assertIs(today_question.was_published_recently(), True)

    def test_was_published_recently_with_yesterdays_date(self):
        time = timezone.now() + datetime.timedelta(hours=-23)
        yesterday_question = Question(pub_date=time)

        self.assertIs(yesterday_question.was_published_recently(), True)

    def test_was_not_published_recently_for_a_day_and_a_minute_ago_is_not_recent(self):
        time = timezone.now() + datetime.timedelta(days=-1) + datetime.timedelta(minutes=-1)
        a_day_and_a_minute_ago = Question(pub_date=time)

        self.assertFalse(a_day_and_a_minute_ago.was_published_recently())

    def test_was_published_recently_for_a_minute_less_than_a_day_ago(self):
        time = timezone.now() + datetime.timedelta(days=-1) + datetime.timedelta(minutes=1)
        a_day_minus_one_minute = Question(pub_date=time)

        self.assertTrue(a_day_minus_one_minute.was_published_recently())

    def test_was_not_published_recently_for_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertFalse(future_question.was_published_recently())
