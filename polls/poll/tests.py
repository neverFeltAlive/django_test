import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """ Creates a question with the given "question_text"
        and time offset to now (days)"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """ Checks if was_published_recently returns accurate data
            for published date in the future """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ Checks if was_published_recently returns accurate data
            for publish date older than 1 day """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ Checks if was_published_recently returns accurate data
            for published date within 1 day """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ Checks if no questions exist and appropriate message is displayed. """
        response = self.client.get(reverse('poll:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """ Checks if questions with a "pub_date" in the past are displayed on the
            index page. """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """ Checks if questions with a "pub_date" in the future aren't displayed on
            the index page. """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('poll:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """ Checks if both past and future questions exist, only past questions
            are displayed. """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """ Checks if the questions index page can display multiple questions. """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """ Checks if the detail view of a question with a "pub_date" in the future
            returns a 404 not found. """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('poll:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ Checks if the detail view of a question with a "pub_date" in the past
            displays the question's text. """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('poll:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

