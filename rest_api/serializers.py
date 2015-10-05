from rest_framework import serializers
from .models import Questionnaire, Category, Question, Answer

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
    answer_groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'question_image', 'categories', 'answer_groups')

class AnswerGroupSerializer(serializers.ModelSerializer):
    """Prepare AnswerGroups for conversion to JSON"""
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = AnswerGroup
        fields = ('id', 'answer_group_name', 'question', 'answers')

class AnswerSerializer(serializers.ModelSerializer):
    """Prepare Answers for conversion to JSON"""
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'score', 'answer_groups')
        