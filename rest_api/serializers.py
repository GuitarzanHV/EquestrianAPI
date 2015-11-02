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
                    'needs_work_score', 'questionnaires', 'subcategories')

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
        fields = ('id', 'name', 'display_text', 'subcategories', 'answers')

class AnswerSerializer(serializers.ModelSerializer):
    """Prepare Answers for conversion to JSON"""
    class Meta:
        model = Answer
        fields = ('id', 'display_text', 'score', 'questions')

class QuestionnaireScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare QuestionnaireScores for conversion to JSON and back"""
    category_scores = serializers.HyperlinkedRelatedField(view_name='categoryscore-detail', many=True, read_only=True)

    class Meta:
        model = QuestionnaireScore
        fields = ('url', 'horse_name', 'horse_owner', 'date_started', 'date_last_edited',
                    'name', 'display_text', 'acceptable_score', 'needs_work_score', 
                    'questionnaire', 'category_scores')
        read_only_fields = ('date_started', 'date_last_edited')

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
            cat_score.save()http://cs3060.bgsu.edu/equestrian-1002/Equestrian_API/blob/master/rest_api/models.py

            for subcategory in cat_score.category.subcategories.all():
                for question in subcategory.questions.all():
                    q_score = QuestionScore(
                        question=question,
                        category_score=cat_score
                    )
                    q_score.save()

        return qnaire_score

class CategoryScoreSerializer(serializers.ModelSerializer):
        read_only_fields = ('date_started', 'date_last_edited', 'name', 
                                'display_text', 'acceptable_score', 
                                'needs_work_score',)

class CategoryScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare CategoryScores for conversion to JSON"""
    subcategory_scores = serializers.HyperlinkedRelatedField(view_name='subcategoryscore-detail', many=True, read_only=True)
    score = serializers.IntegerField(source='get_score', read_only=True)
    evaluation = serializers.CharField(source='get_evaluation', read_only=True)

    class Meta:
        model = CategoryScore
        fields = ('url', 'name', 'display_text', 'acceptable_score', 'needs_work_score', 
                    'score', 'evaluation', 'category', 'questionnaire_score', 'subcategory_scores')

class SubcategoryScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare SubcategoryScores for conversion to JSON and back"""
    question_scores = serializers.HyperlinkedRelatedField(view_name='questionscore-detail', many=True, read_only=True)

    class Meta:
        model = SubcategoryScore
        fields = ('url', 'name', 'display_text', 'subcategory', 'question_scores')

class QuestionScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare QuestionScores for conversion to JSON"""
    answer_scores = serializers.HyperlinkedRelatedField(view_name='answerscore-detail', many=True, read_only=True)

    class Meta:
        model = QuestionScore
        fields = ('id', 'score', 'question', 'answer', 'category_score')
        read_only_fields = ('score', 'question', 'category_score')

    def update(self, instance, validated_data):
        instance.answer = validated_data.get('answer', instance.answer)
        instance.score = validated_data['answer'].score
        instance.save()
        return instance


        
        fields = ('url', 'name', 'display_text', 'question', 'answer', 'subcategory_score', 
                    'answer_scores')
        read_only_fields = ('question', 'subcategory_score', 'name', 'display_text', 'image')

class AnswerScoreSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = AnswerScore
        fields = ('url', 'display_text', 'score', 'answer', 'question_score')
class DefinitionSerializer(serializers.ModelSerializer):
"""Prepare Definitons for JSON
"""
       Definition = serializers.PrimaryKeyRelatedField(many=true, read_only=true)

    class Meta:
        model= Definition
        fields = ("definition_id", "display_word_text","display_definition_text")

