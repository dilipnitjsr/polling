from django.test import TestCase
from django.urls import reverse

from .models import Choice, Question


class PollViewsTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(question_text="Best option?")
        self.choice1 = Choice.objects.create(
            question=self.question, choice_text="A"
        )
        self.choice2 = Choice.objects.create(
            question=self.question, choice_text="B"
        )

    def test_vote_requires_post(self):
        response = self.client.get(
            reverse("polls:vote", args=(self.question.id,))
        )
        self.assertEqual(response.status_code, 405)

    def test_vote_increments_selected_choice(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.id,)),
            {"choice": self.choice1.id},
        )
        self.assertEqual(response.status_code, 302)
        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, 1)

    def test_vote_rejects_choice_from_another_question(self):
        other = Question.objects.create(question_text="Other?")
        other_choice = Choice.objects.create(question=other, choice_text="X")
        response = self.client.post(
            reverse("polls:vote", args=(self.question.id,)),
            {"choice": other_choice.id},
        )
        self.assertEqual(response.status_code, 404)

    def test_create_question_requires_two_choices(self):
        response = self.client.post(
            reverse("polls:add"),
            {
                "question_text": "Only one?",
                "choice1": "A",
                "choice2": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Question.objects.filter(question_text="Only one?").exists()
        )

    def test_create_question_success(self):
        response = self.client.post(
            reverse("polls:add"),
            {
                "question_text": "Two?",
                "choice1": "A",
                "choice2": "B",
            },
        )
        self.assertEqual(response.status_code, 302)
        question = Question.objects.get(question_text="Two?")
        self.assertEqual(question.choice_set.count(), 2)

    def test_votes_api_validates_question_id(self):
        response = self.client.get(reverse("polls:voteapi"))
        self.assertEqual(response.status_code, 400)

    def test_votes_api_returns_choices(self):
        response = self.client.get(
            reverse("polls:voteapi"),
            {"question_id": self.question.id},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["question_text"], "Best option?")
        self.assertEqual(len(payload["choices"]), 2)
