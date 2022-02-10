from django.test import TestCase
from django.contrib.auth.models import User
from control.models import *
from django.test import override_settings

# Create your tests here.

class VotesSecurity(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='u1')
        User.objects.create(username='u2')
        User.objects.create(username='u3')
        with override_settings(USE_TZ=False):
            g1 = Game.objects.create(name="Juego1", expected_start_time="2022-02-01 00:02:20", real_start_time="2022-02-01 00:02:30", finished_time = "2022-02-01 01:02:20", is_active=False)
            g2 = Game.objects.create(name="Juego2", expected_start_time="2022-02-01 00:02:20", real_start_time="2022-02-01 00:02:30", finished_time = "2022-02-01 01:02:20", is_active=False)
        q1 = Question.objects.create(game=g1, question_text="¿Quieres ser millonario?")
        q2 = Question.objects.create(game=g1, question_text="¿Quieres ser millonario?1")
        q3 = Question.objects.create(game=g1, question_text="¿Quieres ser millonario?2")
        q4 = Question.objects.create(game=g2, question_text="¿Quieres ser millonario?3")
        q5 = Question.objects.create(game=g2, question_text="¿Quieres ser millonario?4")
        a1 = Answer_option.objects.create(question=q1, answer_option_text="Si", is_correct = True)
        a2 = Answer_option.objects.create(question=q1, answer_option_text="No", is_correct = False)

    def test_no_double_correct_answer(self):
        """A question can't have two correct answers"""
        q1 = Question.objects.first()
        with self.assertRaises(MultipleCorrectAnswers): 
            Answer_option.objects.create(question=q1, answer_option_text="Ñe", is_correct=True)