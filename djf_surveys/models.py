import itertools
import json
import random, string
from collections import namedtuple

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, gettext

from djf_surveys import app_settings
from djf_surveys.utils import create_star


TYPE_FIELD = namedtuple(
    'TYPE_FIELD', 'text number radio select multi_select text_area url email date rating time date_and_time color json'
)._make(range(14))


def generate_unique_slug(klass, field, id, identifier='slug'):
    """
    Generate unique slug.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    mapping = {
        identifier: unique_slug,
    }
    obj = klass.objects.filter(**mapping).first()
    while obj:
        if obj.id == id:
            break
        rnd_string = random.choices(string.ascii_lowercase, k=(len(unique_slug)))
        unique_slug = '%s-%s-%d' % (origin_slug, ''.join(rnd_string[:10]), numb)
        mapping[identifier] = unique_slug
        numb += 1
        obj = klass.objects.filter(**mapping).first()
    return unique_slug


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Survey(BaseModel):
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), default='')
    slug = models.SlugField(_("slug"), max_length=225, default='')
    editable = models.BooleanField(_("editable"), default=True, help_text=_("If False, user can't edit record."))
    deletable = models.BooleanField(_("deletable"), default=True, help_text=_("If False, user can't delete record."))
    duplicate_entry = models.BooleanField(_("mutiple submissions"), default=False, help_text=_("If True, user can resubmit."))
    private_response = models.BooleanField(_("private response"), default=False, help_text=_("If True, only admin and owner can access."))
    can_anonymous_user = models.BooleanField(_("anonymous submission"), default=False, help_text=_("If True, user without authentatication can submit."))

    class Meta:
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = generate_unique_slug(Survey, self.slug, self.id)
        else:
            self.slug = generate_unique_slug(Survey, self.name, self.id)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")


def get_json_schema_help_text():
    doc_url = "https://django-jsonform.readthedocs.io/en/latest/schema.html"
    doc_url_html = f'<a href="{doc_url}" target="_blank">{doc_url}</a>'
    return mark_safe(gettext("If type of field is JSON, fill in the JSON schema (see %(doc_url)s).") % dict(doc_url=doc_url_html))


class Question(BaseModel):
    TYPE_FIELD = [
        (TYPE_FIELD.text, _("Text")),
        (TYPE_FIELD.number, _("Number")),
        (TYPE_FIELD.radio, _("Radio")),
        (TYPE_FIELD.select, _("Select")),
        (TYPE_FIELD.multi_select, _("Multi Select")),
        (TYPE_FIELD.text_area, _("Text Area")),
        (TYPE_FIELD.url, _("URL")),
        (TYPE_FIELD.email, _("Email")),
        (TYPE_FIELD.date, _("Date")),
        (TYPE_FIELD.time, _("Time")),
        (TYPE_FIELD.date_and_time, _("Date and time")),
        (TYPE_FIELD.rating, _("Rating")),
        (TYPE_FIELD.color, _("Color")),
        (TYPE_FIELD.json, _("JSON")),
    ]

    key = models.CharField(_("key"), max_length=225, unique=True, default="", blank=True,
                           help_text=_("Unique key for this question, fill in the blank if you want to use for automatic generation."))
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE, verbose_name=_("survey"))
    label = models.CharField(_("label"), max_length=500, help_text=_("Enter your question in here."))
    type_field = models.PositiveSmallIntegerField(_("type of input field"), choices=TYPE_FIELD)
    choices = models.TextField(
        _("choices"),
        blank=True, null=True,
        help_text=_("If type of field is radio, select, or multi select, fill in the options separated by commas. Ex: Male, Female.")
    )
    schema = models.JSONField(
        _("schema"),
        blank=True, null=True,
        encoder=DjangoJSONEncoder,
        help_text=get_json_schema_help_text
    )
    help_text = models.CharField(
        _("help text"),
        max_length=200, blank=True, null=True,
        help_text=_("You can add a help text in here.")
    )
    required = models.BooleanField(_("required"), default=True, help_text=_("If True, the user must provide an answer to this question."))
    ordering = models.PositiveIntegerField(_("ordering"), default=0, help_text=_("Defines the question order within the surveys."))

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")
        ordering = ["ordering"]

    def __str__(self):
        return f"{self.label}-survey-{self.survey.id}"

    def save(self, *args, **kwargs):
        if self.key:
            self.key = generate_unique_slug(Question, self.key, self.id, "key")
        else:
            self.key = generate_unique_slug(Question, self.label, self.id, "key")
            
        super(Question, self).save(*args, **kwargs)


class UserAnswer(BaseModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("survey"))
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("user"))
    
    class Meta:
        verbose_name = _("user answer")
        verbose_name_plural = _("user answers")
        ordering = ["-updated_at"]

    def __str__(self):
        return str(self.id)

    def get_user_photo(self):
        if app_settings.SURVEY_USER_PHOTO_PROFILE:
            return eval(app_settings.SURVEY_USER_PHOTO_PROFILE)
        return "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"


class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE, verbose_name=_("question"))
    value = models.TextField(_("value"), help_text=_("The value of the answer given by the user."))
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE, verbose_name=_("user answer"))

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")
        ordering = ["question__ordering"]

    def __str__(self):
        return f"{self.question}: {self.value}"

    @property
    def get_value(self):
        if self.question.type_field == TYPE_FIELD.rating:
            return create_star(active_star=int(self.value))
        elif self.question.type_field == TYPE_FIELD.url:
            return mark_safe(f'<a href="{self.value}" target="_blank">{self.value}</a>')
        elif self.question.type_field == TYPE_FIELD.radio or self.question.type_field == TYPE_FIELD.select or\
                self.question.type_field == TYPE_FIELD.multi_select:
            return self.value.strip().replace("_", " ").capitalize()
        else:
            return self.value

    def get_keys_for_csv(self):
        def getkeys(obj, stack):
            for k, v in obj.items():
                k2 = ([k] if k else []) + stack  # don't return empty keys
                if v and isinstance(v, dict):
                    for c in getkeys(v, k2):
                        yield c
                else:  # leaf
                    yield k2
        question_label = self.question.label
        if self.question.type_field == TYPE_FIELD.json:
            data = json.loads(self.value)
            keys = [f"{question_label} - {k.capitalize()}" for k in itertools.chain.from_iterable(getkeys(data, []))]
        else:
            keys = [question_label]
        return keys

    def get_values_for_csv(self):
        def getvalues(obj):
            for v in obj.values():
                if not v: continue
                if isinstance(v, dict):
                    for c in getvalues(v):
                        yield c
                else:  # leaf
                    yield v if isinstance(v, list) else [v]

        if self.question.type_field == TYPE_FIELD.radio or self.question.type_field == TYPE_FIELD.select or\
                self.question.type_field == TYPE_FIELD.multi_select:
            values = [self.value.strip().replace("_", " ").capitalize()]
        elif self.question.type_field == TYPE_FIELD.json:
            data = json.loads(self.value)
            values = list(itertools.chain.from_iterable(getvalues(data)))
        else:
            values = [self.value.strip()]
        return values
