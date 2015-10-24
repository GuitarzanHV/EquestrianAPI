from rest_framework import serializers 
from .models import *

class QuestionnaireSerializer(serializers.ModelSerializer):
    """Prepare Questionnaires for conversion to JSON"""
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'name', 'display_text', 'acceptable_score', 
                    'needs_work_score', 'categories')

class CategorySerializer(serializers.ModelSerializer):
    """Prepare Catgories for conversion to JSON"""
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'display_text', 'acceptable_score', 
                    'needs_work_score', 'questionnaires', 'questions')

class SubcategorySerializer(serializers.ModelSerializer):
    """Prepare Subcategories for JSON"""
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'display_text', 'categories', 'questions')

class QuestionSerializer(serializers.ModelSerializer):
    """Prepare Questions for conversion to JSON"""
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'name', 'display_text', 'question_image', 'subcategories', 'answers')

class AnswerSerializer(serializers.ModelSerializer):
    """Prepare Answers for conversion to JSON"""
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'score', 'questions')

class QuestionnaireScoreSerializer(serializers.ModelSerializer):
    """Prepare Horses for conversion to JSON"""
    category_scores = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = QuestionnaireScore
        fields = ('id', 'name', 'owner', 'date_started', 'date_last_edited',
                    'questionnaire', 'category_scores')

    def create(self, validated_data):
        qnaire_score = QuestionnaireScore(
            name=validated_data['name'],
            owner=validated_data['owner'],
            questionnaire=validated_data['questionnaire']
        )
        qnaire_score.save()

        for category in qnaire_score.questionnaire.categories.all():
            cat_score = CategoryScore(
                category=category,
                questionnaire_score=qnaire_score
            )
            cat_score.save()

            for subcategory in cat_score.category.subcategories.all():
                for question in subcategory.questions.all():
                    q_score = QuestionScore(
                        question=question,
                        category_score=cat_score
                    )
                    q_score.save()

        return qnaire_score

class CategoryScoreSerializer(serializers.ModelSerializer):
    """Prepare CategoryScores for conversion to JSON"""
    question_scores = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CategoryScore
        fields = ('id', 'score', 'evaluation', 'category', 'questionnaire_score', 'question_scores')

class QuestionScoreSerializer(serializers.ModelSerializer):
    """Prepare QuestionScores for conversion to JSON"""
    class Meta:
        model = QuestionScore
        fields = ('id', 'score', 'evaluation', 'question', 'answer', 'category_score')
        