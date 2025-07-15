import re
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import MaxValueValidator, validate_comma_separated_integer_list
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
# Supprimé: from django.utils.encoding import python_2_unicode_compatible (obsolète dans Django 4.0+)

from model_utils.managers import InheritanceManager


class CategoryManager(models.Manager):

    def new_category(self, category):
        new_category = self.create(category=re.sub(r'\s+', '-', category)
                                   .lower())

        new_category.save()
        return new_category


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class Category(models.Model):

    category = models.CharField(
        verbose_name=_("Category"),
        max_length=250, blank=True,
        unique=True, null=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.category


class SubCategoryManager(models.Manager):

    def new_subcategory(self, subcategory, category):
        new_subcategory = self.create(sub_category=re.sub(r'\s+', '-', subcategory)
                                      .lower(),
                                      category=category)

        new_subcategory.save()
        return new_subcategory


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class SubCategory(models.Model):

    sub_category = models.CharField(
        verbose_name=_("Sub-Category"),
        max_length=250, blank=True, null=True)

    category = models.ForeignKey(
        Category, null=True, blank=True,
        verbose_name=_("Category"), on_delete=models.CASCADE)

    objects = SubCategoryManager()

    class Meta:
        verbose_name = _("Sub-Category")
        verbose_name_plural = _("Sub-Categories")

    def __str__(self):
        return self.sub_category


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class Quiz(models.Model):

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=60, blank=False)

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("a description of the quiz"))

    url = models.SlugField(
        max_length=60, blank=False,
        help_text=_("a user friendly url"),
        verbose_name=_("user friendly url"))

    category = models.ForeignKey(
        Category, null=True, blank=True,
        verbose_name=_("Category"), on_delete=models.CASCADE)

    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name=_("Random Order"),
        help_text=_("Display the questions in "
                    "a random order or as they "
                    "were added."))

    max_questions = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Max Questions"),
        help_text=_("Number of questions to be answered on each attempt."))

    answers_at_end = models.BooleanField(
        blank=False, default=False,
        help_text=_("Correct answer is NOT shown after question."
                    " Answers displayed at the end."),
        verbose_name=_("Answers at end"))

    exam_paper = models.BooleanField(
        blank=False, default=False,
        help_text=_("If yes, the result of each"
                    " attempt by a user will be"
                    " stored. Necessary for marking."),
        verbose_name=_("Exam paper"))

    single_attempt = models.BooleanField(
        blank=False, default=False,
        help_text=_("If yes, only one attempt by"
                    " a user will be permitted."
                    " Non users cannot sit this exam."),
        verbose_name=_("Single Attempt"))

    pass_mark = models.SmallIntegerField(
        blank=True, default=0,
        verbose_name=_("Pass Mark"),
        help_text=_("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)])

    success_text = models.TextField(
        blank=True, help_text=_("Displayed if user passes."),
        verbose_name=_("Success Text"))

    fail_text = models.TextField(
        verbose_name=_("Fail Text"),
        blank=True, help_text=_("Displayed if user fails."))

    draft = models.BooleanField(
        blank=True, default=False,
        verbose_name=_("Draft"),
        help_text=_("If yes, the quiz is not displayed"
                    " in the quiz list and can only be"
                    " taken by users who can edit"
                    " quizzes."))

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.url = re.sub(r'\s+', '-', self.url).lower()

        self.url = ''.join(letter for letter in self.url if
                           letter.isalnum() or letter == '-')

        if self.single_attempt is True:
            self.exam_paper = True

        if self.pass_mark > 100:
            raise ValidationError('%s is above 100' % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all().select_subclasses()

    @property
    def get_max_score(self):
        return self.get_questions().count()

    def anon_score_id(self):
        return str(self.id) + "_score"

    def anon_q_list(self):
        return str(self.id) + "_q_list"

    def anon_q_data(self):
        return str(self.id) + "_data"


class ProgressManager(models.Manager):

    def new_progress(self, user):
        new_progress = self.create(user=user,
                                   score="")
        new_progress.save()
        return new_progress


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class Progress(models.Model):
    """
    Progress is used to track an individual signed in users score on different
    quiz's and categories

    Data stored in csv using the format:
        category, score, possible, category, score, possible, ...
    """
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)

    score = models.TextField(
        verbose_name=_("Score"),
        max_length=1024,
        validators=[validate_comma_separated_integer_list])

    objects = ProgressManager()

    class Meta:
        verbose_name = _("User Progress")
        verbose_name_plural = _("User progress records")

    def __str__(self):
        return f"{self.user.username} - {self.score}"

    @property
    def list_all_cat_scores(self):
        """
        Returns a list of score strings
        """
        score_before = self.score
        output = {}

        for x in score_before.split(','):
            try:
                cat = Category.objects.get(category=x)
                score = score_before.split(x)[1].split(',')[1]
                output[cat] = score

            except Category.DoesNotExist:
                pass

        return output

    def update_score(self, question, score_to_add=0, possible_to_add=0):
        """
        Updates the progress score
        """
        category_test = Category.objects.filter(category=question.category)\
                                        .exists()

        if category_test:

            to_find = re.escape(str(question.category)) + r",(?P<score>\d+),(?P<possible>\d+),"

            match = re.search(to_find, self.score, re.IGNORECASE)

            if match:
                updated_score = int(match.group('score')) + abs(score_to_add)
                updated_possible = int(match.group('possible')) + abs(possible_to_add)

                new_score = f",{updated_score},{updated_possible},"

                self.score = re.sub(to_find, new_score, self.score,
                                    flags=re.IGNORECASE)
            else:
                self.score += f"{question.category},{score_to_add},{possible_to_add},"

        self.save()

    def show_exams(self):
        """
        Finds the previous quizzes marked as 'exam papers'.
        Returns a queryset of complete quizzes.
        """
        return Sitting.objects.filter(user=self.user, complete=True)


class SittingManager(models.Manager):

    def new_sitting(self, user, quiz):
        if quiz.random_order is True:
            question_set = quiz.question_set.all() \
                .select_subclasses() \
                .order_by('?')
        else:
            question_set = quiz.question_set.all() \
                .select_subclasses()

        question_set = [item.id for item in question_set]

        if quiz.max_questions and quiz.max_questions < len(question_set):
            question_set = question_set[:quiz.max_questions]

        questions = ",".join(map(str, question_set)) + ","

        new_sitting = self.create(user=user,
                                  quiz=quiz,
                                  question_list=questions,
                                  incorrect_questions="",
                                  current_score=0,
                                  complete=False,
                                  user_answers='{}')
        return new_sitting

    def user_sitting(self, user, quiz):
        if quiz.single_attempt is True \
           and self.filter(user=user, quiz=quiz, complete=True).exists():
            return False

        try:
            sitting = self.get(user=user, quiz=quiz, complete=False)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user, quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(user=user, quiz=quiz, complete=False)[0]
        return sitting


# Django 5.2.4 - plus besoin de @python_2_unicode_compatible
class Sitting(models.Model):
    """
    Used to store the progress of logged in users sitting a quiz.
    Replaces the session system used by anon users.
    """

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, verbose_name=_("Quiz"), on_delete=models.CASCADE)

    question_list = models.TextField(
        verbose_name=_("Question List"),
        validators=[validate_comma_separated_integer_list])

    incorrect_questions = models.TextField(
        verbose_name=_("Incorrect questions"),
        blank=True)

    current_score = models.IntegerField(verbose_name=_("Current Score"))

    complete = models.BooleanField(default=False, blank=False,
                                   verbose_name=_("Complete"))

    user_answers = models.TextField(blank=True, default='{}',
                                    verbose_name=_("User Answers"))

    start = models.DateTimeField(auto_now_add=True,
                                 verbose_name=_("Start"))

    end = models.DateTimeField(null=True, blank=True, verbose_name=_("End"))

    objects = SittingManager()

    class Meta:
        permissions = (("view_sittings", "Can see completed exams."),)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

    def get_first_question(self):
        """
        Returns the next question.
        If no question is found, returns False
        Does NOT remove the question from the front of the list.
        """
        if not self.question_list:
            return False

        first, _ = self.question_list.split(',', 1)
        question_id = int(first)
        return Question.objects.get_subclass(id=question_id)

    def remove_first_question(self):
        if not self.question_list:
            return

        _, others = self.question_list.split(',', 1)
        self.question_list = others
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(n) for n in self.question_list.split(',') if n]

    @property
    def get_percent_correct(self):
        dividend = float(self.current_score)
        divisor = len(self._question_ids())
        if divisor < 1:
            return 0            # Prevent divide by zero error

        if dividend > divisor:
            return 100

        correct = int(round((dividend / divisor) * 100))

        if correct >= 1:
            return correct
        else:
            return 0

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_incorrect_question(self, question):
        """
        Adds uid of incorrect question to the list.
        The question object must be passed in.
        """
        if len(self.incorrect_questions) > 0:
            self.incorrect_questions += ','
        self.incorrect_questions += str(question.id) + ","
        if self.complete:
            self.add_to_score(-1)
        self.save()

    @property
    def get_incorrect_questions(self):
        """
        Returns a list of non empty integers, representing the pk of
        questions
        """
        return [int(q) for q in self.incorrect_questions.split(',') if q]

    def remove_incorrect_question(self, question):
        current = self.get_incorrect_questions
        current.remove(question.id)
        self.incorrect_questions = ','.join(map(str, current))
        self.add_to_score(1)
        self.save()

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        if self.check_if_passed:
            return self.quiz.success_text
        else:
            return self.quiz.fail_text

    def add_user_answer(self, question, guess):
        current = json.loads(self.user_answers)
        current[question.id] = guess
        self.user_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers=False):
        question_ids = self._question_ids()
        questions = sorted(
            self.quiz.question_set.filter(id__in=question_ids)
                                  .select_subclasses(),
            key=lambda q: question_ids.index(q.id))

        if with_answers:
            user_answers = json.loads(self.user_answers)
            for question in questions:
                question.user_answer = user_answers[question.id]

        return questions


class Question(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """

    quiz = models.ForeignKey(Quiz, verbose_name=_("Quiz"), on_delete=models.CASCADE)

    category = models.ForeignKey(Category, verbose_name=_("Category"),
                                 blank=True, null=True, on_delete=models.CASCADE)

    sub_category = models.ForeignKey(SubCategory, verbose_name=_("Sub-Category"),
                                     blank=True, null=True, on_delete=models.CASCADE)

    figure = models.ImageField(upload_to='uploads/%Y/%m/%d',
                              blank=True,
                              null=True,
                              verbose_name=_("Figure"))

    content = models.TextField(max_length=1000,
                              blank=False,
                              help_text=_("Enter the question text that "
                                          "you want displayed"),
                              verbose_name=_('Question'))

    explanation = models.TextField(max_length=2000,
                                  blank=True,
                                  help_text=_("Explanation to be shown "
                                              "after the question has "
                                              "been answered."),
                                  verbose_name=_('Explanation'))

    objects = InheritanceManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['category']

    def __str__(self):
        return self.content