from django.contrib import admin
from .models import Questionnaire, Category, Question, Answer

# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(AnswerGroup)
admin.site.register(Answer)
