from django.contrib import admin

from .admins.forms import QuestionForm
from .models import Survey, Question, Answer, UserAnswer


class AdminQuestionForm(QuestionForm):
    class Meta(QuestionForm.Meta):
        fields = fields = ['survey', 'label', 'key', 'type_field', 'choices', 'schema', 'help_text', 'required']


class AdminQuestion(admin.ModelAdmin):
    list_display = ('survey', 'label', 'type_field', 'required', 'ordering')
    list_editable = ('label', 'required', 'ordering')
    search_fields = ('survey', )
    form = AdminQuestionForm
    list_select_related = ['survey']
    list_filter = ['survey']
    save_as = True
    save_on_top = True


class AdminAnswer(admin.ModelAdmin):
    list_display = ('question', 'get_label', 'value', 'user_answer')
    search_fields = ('question__label', 'value',)
    list_filter = ('question__survey',)
    list_select_related = ['question']

    def get_label(self, obj):
        return obj.question.label
    get_label.admin_order_field = 'question'
    get_label.short_description = 'Label'


class AdminUserAnswer(admin.ModelAdmin):
    list_display = ('survey', 'user', 'created_at', 'updated_at')
    list_select_related = ['survey', 'user']


class AdminSurvey(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'slug', 'editable', 'deletable', 'duplicate_entry', 'private_response', 'can_anonymous_user')
    list_editable = ('name', 'slug', 'editable', 'deletable', 'duplicate_entry', 'private_response', 'can_anonymous_user')
    exclude = ['slug']
    save_as = True
    save_on_top = True


admin.site.register(Survey, AdminSurvey)
admin.site.register(Question, AdminQuestion)
admin.site.register(Answer, AdminAnswer)
admin.site.register(UserAnswer, AdminUserAnswer)
