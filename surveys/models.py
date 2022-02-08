from collections import namedtuple

from django.db import models
from django.contrib.auth import get_user_model


TYPE_FIELD = namedtuple(
    'TYPE_FIELD', 'text number radio select multi_select text_area'
)._make(range(6))


class Survey(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPE_FIELD = [(TYPE_FIELD.text, "text"), (TYPE_FIELD.number, "number"),
                  (TYPE_FIELD.radio, "radio"), (TYPE_FIELD.select, "select"),
                  (TYPE_FIELD.multi_select, "multi select"), (TYPE_FIELD.text_area, "text area")]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    label = models.CharField(max_length=200, help_text='Enter your question in here')
    type_field = models.PositiveSmallIntegerField(choices=TYPE_FIELD)
    choices = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='if Type Field is (radio, select, multi select), fill in the option separated by commas. ex: Male, Female'
    )
    help_text = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='You can add a help text in here'
    )
    required = models.BooleanField(default=True)

    def __str__(self):
        return self.survey.name


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.question}: {self.value}'

    @classmethod
    def get_answer(cls, survey, user=None):
        question_ids = Question.objects.filter(survey=survey).values_list('id', flat=True)
        return cls.objects.filter(user=user, question_id__in=question_ids)