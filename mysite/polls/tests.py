import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Create your tests here.


class QuestionModelsTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns false for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_older_question(self):
        """
        was_published_recently() returns False for all questions whose pub_date is older than one day
        """
        time = timezone.now() - datetime.timedelta(days=3)
        older_question = Question(pub_date=time)
        self.assertIs(older_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for all questions whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
    

def create_question(question_text, days):
    """
    create_question() returns sample Question object for many test methods
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """
        if no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self. assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_past_question(self):
        """
        questions with a pub_date in the past are displayed on the index page
        """
        create_question(question_text="Past question sample", days=-30 )
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question sample>'])
    
    def test_future_question(self):
        """
        questions with a pub_date in the future are not displayed on the index page
        """
        create_question(question_text="Sample question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_two_past_questions(self):
        """
        check if all past questions are displayed on the index page
        """
        create_question(question_text="Question three", days=-10)
        create_question(question_text="Question four", days=-15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            ['<Question: Question four>', '<Question: Question three>'])

    def test_future_and_past_questions(self):
        """
        questions in pub_date in the future are not displayed but questions
        in pub_date from the past are displayed on index page
        """
        create_question(question_text="Past question", days=-20)
        create_question(question_text="Future question", days=20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        A detail view of a question with pub_date in the future returns a 404 error
        """
        future_question = create_question(question_text="Future question", days=20)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        The detail view of a questions with pub_date in the past returns a question text
        """
        past_question = create_question(question_text="Past question", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTest(TestCase):
    def test_past_question(self):
        past_question = create_question(question_text="Another past", days=-20)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_future_question(self):
        future_question = create_question(question_text="Another future", days=2)
        url=reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)