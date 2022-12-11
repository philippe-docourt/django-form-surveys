from django.forms import ModelForm
from django_json_widget.widgets import JSONEditorWidget

from djf_surveys.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['label', 'key', 'type_field', 'choices', 'schema', 'help_text', 'required']
        widgets = {
            'schema': JSONEditorWidget(width="100%", height="450px")
        }
