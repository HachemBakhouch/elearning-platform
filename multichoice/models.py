from django.db import models
# Supprimé: from django.utils.encoding import python_2_unicode_compatible (obsolète dans Django 4.0+)
from django.utils.translation import gettext_lazy as _

from quiz.models import Question


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class MCQuestion(Question):

    answer_order = models.CharField(
        max_length=30, null=True, blank=True,
        choices=(('content', _('Content')),
                 ('random', _('Random')),
                 ('none', _('None'))),
        help_text=_("The order in which multichoice "
                    "answer options are displayed "
                    "to the user"),
        verbose_name=_("Answer Order"))

    def check_if_correct(self, guess):
        answer = Answer.objects.get(id=guess)

        if answer.correct is True:
            return True
        else:
            return False

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by()
        return queryset

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question=self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in
                self.order_answers(Answer.objects.filter(question=self))]

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class Answer(models.Model):
    question = models.ForeignKey(MCQuestion, verbose_name=_("Question"), on_delete=models.CASCADE)

    content = models.CharField(max_length=1000,
                              blank=False,
                              help_text=_("Enter the answer text that "
                                          "you want displayed"),
                              verbose_name=_("Content"))

    correct = models.BooleanField(blank=False,
                                 default=False,
                                 help_text=_("Is this a correct answer?"),
                                 verbose_name=_("Correct"))

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")