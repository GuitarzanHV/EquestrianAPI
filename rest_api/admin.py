from django.contrib import admin
from .models import Questionnaire
from .models import Category
from .models import Question
from .models import Answer

# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
