from django.db import models
# Supprimé: from django.utils.encoding import python_2_unicode_compatible (obsolète dans Django 4.0+)
from django.utils.translation import gettext_lazy as _

from quiz.models import Question


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class Essay_Question(Question):

    def check_if_correct(self, guess):
        return False

    def get_answers(self):
        return False

    def get_answers_list(self):
        return False

    def answer_choice_to_string(self, guess):
        return str(guess)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Essay style question")
        verbose_name_plural = _("Essay style questions")