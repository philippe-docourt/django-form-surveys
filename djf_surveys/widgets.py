from django import forms
from django_jsonform.widgets import JSONFormWidget


class CheckboxSelectMultipleSurvey(forms.CheckboxSelectMultiple):
    option_template_name = 'djf_surveys/widgets/checkbox_option.html'


class RadioSelectSurvey(forms.RadioSelect):
    option_template_name = 'djf_surveys/widgets/radio_option.html'


class DateSurvey(forms.DateTimeInput):
    template_name = 'djf_surveys/widgets/datepicker.html'


class TimeSurvey(forms.TimeInput):
    template_name = 'djf_surveys/widgets/timepicker.html'


class DateTimeSurvey(forms.DateTimeInput):
    template_name = 'djf_surveys/widgets/datetimepicker.html'


class RatingSurvey(forms.HiddenInput):
    template_name = 'djf_surveys/widgets/star_rating.html'


class ColorSurvey(forms.HiddenInput):
    template_name = 'djf_surveys/widgets/colorpicker.html'


class ColorSurvey(forms.HiddenInput):
    template_name = 'djf_surveys/widgets/colorpicker.html'


class SurveyJSONFormWidget(JSONFormWidget):
    template_name = 'django_jsonform/editor.html'

    @property
    def media(self):
        css = {
            'all': [
                'djf_surveys/css/rjf.css',
            ]
        }
        all_media = super().media
        override_media = forms.Media(css=css)
        all_media += override_media
        return all_media
