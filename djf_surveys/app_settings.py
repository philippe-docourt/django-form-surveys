from django.conf import settings
# replace master template
SURVEY_MASTER_TEMPLATE = settings.SURVEY_MASTER_TEMPLATE if hasattr(settings,
                                                                    'SURVEY_MASTER_TEMPLATE') else 'djf_surveys/master.html'

# profile photo path
SURVEY_USER_PHOTO_PROFILE = settings.SURVEY_USER_PHOTO_PROFILE if hasattr(settings, 'SURVEY_USER_PHOTO_PROFILE') else ""

# date and time input format
DATE_INPUT_FORMATS = settings.DATE_INPUT_FORMATS if hasattr(settings, 'DATE_INPUT_FORMATS') else \
    ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d/%m/%y', '%d/%m/%Y']

TIME_INPUT_FORMATS = settings.TIME_INPUT_FORMATS if hasattr(settings, 'TIME_INPUT_FORMATS') else \
    [
        '%H:%M:%S',  # '14:30:59'
        '%H:%M',  # '14:30'
    ]

DATETIME_INPUT_FORMATS = settings.DATETIME_INPUT_FORMATS if hasattr(settings, 'DATETIME_INPUT_FORMATS') else \
[
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
]

# validators
field_validators = {
    'max_length': {
        'email': 150,
        'text': 250,
        'url': 250
    }
}
if hasattr(settings, 'SURVEY_FIELD_VALIDATORS'):
    max_length = settings.SURVEY_FIELD_VALIDATORS.get('max_length')
    if max_length:
        field_validators['max_length'].update(max_length)
SURVEY_FIELD_VALIDATORS = field_validators

# charjs source
CHART_JS_SRC = settings.CHART_JS_SRC if hasattr(settings, 'CHART_JS_SRC') else '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'

# number of pagination
number_of_pagination = {
    'survey_list': 12,
    'answer_list': 12 
}
if hasattr(settings, 'SURVEY_PAGINATION_NUMBER'):
    survey_list = settings.SURVEY_PAGINATION_NUMBER.get('survey_list')
    if survey_list:
        number_of_pagination['survey_list'] = survey_list
        
    answer_list = settings.SURVEY_PAGINATION_NUMBER.get('answer_list')
    if answer_list:
        number_of_pagination['answer_list'] = answer_list
SURVEY_PAGINATION_NUMBER = number_of_pagination

SURVEYS_ADMIN_BASE_PATH = "dashboard/"