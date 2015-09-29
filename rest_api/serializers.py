from rest_framework import serializers
from .models import Questionnaire, Category, Question, Answer

class QuestionnaireSerializer(serializers.ModelSerializer):
    """docstring for ClassName"""
    class Meta:
        model = Questionnaire
        fields = ('id', 'questionnaire_name', 'acceptable_score', 'needs_work_score', 'unacceptable_score')

class CategorySerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'acceptable_score', 'needs_work_score', 'unacceptable_score', 'questionnaires')

class QuestionSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'question_image', 'categories')

class AnswerSerializer(serializers.ModelSerializer):
    """docstring"""
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'score', 'question')
        