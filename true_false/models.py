from django.db import models
# Supprimé: from django.utils.encoding import python_2_unicode_compatible (obsolète dans Django 4.0+)
from django.utils.translation import gettext_lazy as _

from quiz.models import Question


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class TF_Question(Question):

    correct = models.BooleanField(blank=False,
                                 default=False,
                                 help_text=_("Is the answer True or False"),
                                 verbose_name=_("Correct"))

    def check_if_correct(self, guess):
        if guess == "True":
            guess_bool = True
        elif guess == "False":
            guess_bool = False
        else:
            return False

        if guess_bool == self.correct:
            return True
        else:
            return False

    def get_answers(self):
        return [{'correct': self.check_if_correct("True"),
                'content': 'True'},
                {'correct': self.check_if_correct("False"),
                'content': 'False'}]

    def get_answers_list(self):
        return [(True, True), (False, False)]

    def answer_choice_to_string(self, guess):
        return str(guess)

    class Meta:
        verbose_name = _("True/False Question")
        verbose_name_plural = _("True/False Questions")