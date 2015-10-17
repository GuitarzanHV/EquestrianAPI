from rest_framework import serializers 
from .models import *

class QuestionnaireSerializer(serializers.ModelSerializer):
    """Prepare Questionnaires for conversion to JSON"""
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'questionnaire_name', 'needs_work_score', 
            'unacceptable_score', 'categories')

class CategorySerializer(serializers.ModelSerializer):
    """Prepare Catgories for conversion to JSON"""
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'category_name', 'needs_work_score', 
            'unacceptable_score', 'questionnaires', 'questions')

class QuestionSerializer(serializers.ModelSerializer):
    """Prepare Questions for conversion to JSON"""
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question_name', 'question_text', 'question_image', 'categories', 'answers')

class AnswerSerializer(serializers.ModelSerializer):
    """Prepare Answers for conversion to JSON"""
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'score', 'questions')

class QuestionnaireScoreSerializer(serializers.ModelSerializer):
    """Prepare Horses for conversion to JSON"""
    category_scores = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    score = serializers.IntegerField(default=category_score_total(), read_only=True)

    class Meta:
        model = Horse
        fields = ('id', 'name', 'score', 'owner', 'questionnaire', 'category_scores')

class CategoryScoreSerializer(serializers.ModelSerializer):
    """Prepare CategoryScores for conversion to JSON"""
    question_scores = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    score = serializers.IntegerField(default=question_score_total(), read_only=True)

    class Meta:
        model = CategoryScore
        fields = ('id', 'score', 'category', 'questionnaire_score', 'question_scores')

class QuestionScoreSerializer(serializers.ModelSerializer):
    """Prepare QuestionScores for conversion to JSON"""
    class Meta:
        model = QuestionScore
        fields = ('id', 'score', 'question', 'answer', 'category_score')
        