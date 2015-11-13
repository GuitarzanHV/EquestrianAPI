from django.contrib.auth.models import User
from rest_framework import serializers 
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    questionnaire_scores = serializers.HyperlinkedRelatedField(view_name='questionnairescore-detail', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'questionnaire_scores')


class QuestionnaireSerializer(serializers.ModelSerializer):
    """Prepare Questionnaires for conversion to JSON"""
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = (
            'id', 'name', 'display_text', 'mobile', 
            'acceptable_score', 'needs_work_score', 'categories'
            )


class CategorySerializer(serializers.ModelSerializer):
    """Prepare Catgories for conversion to JSON"""
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'display_text', 'acceptable_score', 
            'needs_work_score', 'questionnaires', 'subcategories'
            )


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
        fields = ('id', 'name', 'display_text', 'subcategory', 'answers')


class AnswerSerializer(serializers.ModelSerializer):
    """Prepare Answers for conversion to JSON"""
    class Meta:
        model = Answer
        fields = ('id', 'display_text', 'score', 'question')


class QuestionnaireScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare QuestionnaireScores for conversion to JSON and back"""
    category_scores = serializers.HyperlinkedRelatedField(view_name='categoryscore-detail', many=True, read_only=True)

    class Meta:
        model = QuestionnaireScore
        fields = ('url', 'horse_name', 'horse_owner', 
            'location', 'score', 'evaluation', 'date_started', 
            'date_last_edited', 'name', 'display_text', 
            'acceptable_score', 'needs_work_score', 'questionnaire', 
            'category_scores'
            )
        read_only_fields = ('name', 'display_text', 'acceptable_score', 
            'needs_work_score', 'date_started', 'date_last_edited'
            )

    def create(self, validated_data):
        qnaire_score = QuestionnaireScore(
            horse_name=validated_data['horse_name'],
            horse_owner=validated_data['horse_owner'],
            location=validated_data['location'],
            questionnaire=validated_data['questionnaire']
            )
        qnaire_score.name = qnaire_score.questionnaire.name
        qnaire_score.display_text = qnaire_score.questionnaire.display_text
        qnaire_score.acceptable_score = qnaire_score.questionnaire.acceptable_score
        qnaire_score.needs_work_score = qnaire_score.questionnaire.needs_work_score
        qnaire_score.mobile = qnaire_score.questionnaire.mobile
        qnaire_score.save()

        for category in qnaire_score.questionnaire.categories.all():
            cat_score = CategoryScore(
                category=category,
                questionnaire_score=qnaire_score
            )
            cat_score.name = cat_score.category.name
            cat_score.display_text = cat_score.category.display_text
            cat_score.acceptable_score = cat_score.category.acceptable_score
            cat_score.needs_work_score = cat_score.category.needs_work_score
            cat_score.save()

            for subcategory in cat_score.category.subcategories.all():
                subcat_score = SubcategoryScore(
                    subcategory=subcategory,
                    category_score=cat_score
                )
                subcat_score.name = subcat_score.subcategory.name
                subcat_score.display_text = subcat_score.subcategory.display_text
                subcat_score.save()

                for question in subcategory.questions.all():
                    q_score = QuestionScore(
                        question=question,
                        subcategory_score=subcat_score
                    )
                    q_score.name = q_score.question.name
                    q_score.display_text = q_score.question.display_text
                    #q_score.image = q_score.question.image
                    q_score.save()

                    for answer in question.answers.all():
                        a_score = AnswerScore(
                            answer=answer,
                            question_score=q_score
                        )
                        a_score.display_text = a_score.answer.display_text
                        a_score.score = a_score.answer.score
                        a_score.save()

        return qnaire_score


class CategoryScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare CategoryScores for conversion to JSON"""
    subcategory_scores = serializers.HyperlinkedRelatedField(view_name='subcategoryscore-detail', many=True, read_only=True)

    class Meta:
        model = CategoryScore
        fields = ('url', 'name', 'display_text', 
            'acceptable_score', 'needs_work_score', 'score', 
            'evaluation', 'category', 'questionnaire_score', 
            'subcategory_scores'
            )
        read_only_fields = ('date_started', 'date_last_edited', 'name', 
            'display_text', 'acceptable_score', 'needs_work_score',
            )


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
        fields = ('url', 'question', 'answer', 'subcategory_score', 'answer_scores')
        read_only_fields = ('question', 'subcategory_score', 'answer_scores')


class AnswerScoreSerializer(serializers.HyperlinkedModelSerializer):
    "Prepare AnswerScores for conversion to JSON"
    class Meta:
        model = AnswerScore
        fields = ('url', 'display_text', 'score', 'answer', 'question_score')


class QuestionnaireScoreNestedSerializer(serializers.ModelSerializer):
    """Nested serializer for uploading QuestionnaireScores from mobile"""
    class Meta:
        model = QuestionnaireScore
        depth = 5


class DefinitionSerializer(serializers.ModelSerializer):
    """Prepare Definitons for JSON"""
    class Meta:
        model= Definition
        fields = ("id", "display_word_text", "display_definition_text")

