from django.contrib.auth.models import User
from rest_framework import serializers 
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    "Serialize django User class for OAuth and login"
    questionnaire_scores = serializers.HyperlinkedRelatedField(view_name='questionnairescore-detail', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'questionnaire_scores')


#Questionnaire tree serializers. Used by the mobile versions for uploading raw data.
class QuestionnaireSerializer(serializers.ModelSerializer):
    """Prepare Questionnaires for conversion to JSON"""
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = (
            'id', 'name', 'display_text',
            'mobile', 'riding_style', 'acceptable_score',
            'needs_work_score', 'categories'
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


#QuestionnaireScore tree serializers. Used by the website for displaying and saving scores
class QuestionnaireScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare QuestionnaireScores for conversion to JSON and back"""
    category_scores = serializers.HyperlinkedRelatedField(view_name='categoryscore-detail', many=True, read_only=True)
    questionnaire = serializers.HyperlinkedRelatedField(queryset=Questionnaire.objects.all(), view_name='questionnaire-detail')

    class Meta:
        model = QuestionnaireScore
        fields = ('url', 'horse_name', 'horse_owner', 
            'location', 'score', 'evaluation', 'date_started', 
            'date_last_edited', 'name', 'display_text', 
            'riding_style', 'acceptable_score', 'needs_work_score', 
            'questionnaire', 'category_scores'
            )
        read_only_fields = ('name', 'display_text', 'riding_style',
            'acceptable_score', 'needs_work_score', 'date_started', 
            'date_last_edited'
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
        qnaire_score.riding_style = qnaire_score.questionnaire.riding_style
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


class SubcategoryScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare SubcategoryScores for conversion to JSON and back"""
    question_scores = serializers.HyperlinkedRelatedField(view_name='questionscore-detail', many=True, read_only=True)

    class Meta:
        model = SubcategoryScore
        fields = ('url', 'name', 'display_text', 'subcategory', 'category_score', 'question_scores')


class QuestionScoreSerializer(serializers.HyperlinkedModelSerializer):
    """Prepare QuestionScores for conversion to JSON"""
    answer_scores = serializers.HyperlinkedRelatedField(view_name='answerscore-detail', many=True, read_only=True)
    id = serializers.HiddenField(default='0')

    class Meta:
        model = QuestionScore
        fields = ('url', 'name', 'display_text', 
            'question', 'answer', 'subcategory_score', 
            'answer_scores', 'id'
            )
        read_only_fields = ('name', 'display_text', 'question', 'subcategory_score', 'answer_scores')

    def __init__(self, *args, **kwargs):
        super(QuestionScoreSerializer, self).__init__(*args, **kwargs)
        #print(str(self.fields['id'].get_attribute(self.instance)))
        self.fields['answer'].queryset = AnswerScore.objects.filter(question_score__pk=self.fields['id'].get_attribute(self.instance))


class AnswerScoreSerializer(serializers.HyperlinkedModelSerializer):
    "Prepare AnswerScores for conversion to JSON"
    class Meta:
        model = AnswerScore
        fields = ('url', 'display_text', 'score', 'answer', 'question_score')


#Nested QuestionnaireScore serializers. For mobile platforms to upload completed forms.
class AnswerScoreNestedSerializer(serializers.ModelSerializer):
    "Nested AnswerScore serializer for nested views"
    class Meta:
        model = AnswerScore
        fields = ('pk', 'display_text', 'score', 'answer', 'question_score')


class QuestionScoreNestedSerializer(serializers.ModelSerializer):
    """Nested QuestionScore serializer for nested views"""
    answer_scores = AnswerScoreNestedSerializer(many=True)

    class Meta:
        model = QuestionScore
        fields = ('pk', 'name', 'display_text',
            'question', 'answer', 'subcategory_score', 
            'answer_scores'
            )


class SubcategoryScoreNestedSerializer(serializers.ModelSerializer):
    """Nested SubcategoryScore serializer for nested views"""
    question_scores = QuestionScoreNestedSerializer(many=True)

    class Meta:
        model = SubcategoryScore
        fields = ('pk', 'name', 'display_text', 'subcategory', 'category_score', 'question_scores')


class CategoryScoreNestedSerializer(serializers.ModelSerializer):
    """Nested CategoryScore Serializer for nested views"""
    subcategory_scores = SubcategoryScoreNestedSerializer(many=True)

    class Meta:
        model = CategoryScore
        fields = ('pk', 'name', 'display_text', 
            'acceptable_score', 'needs_work_score', 'score', 
            'evaluation', 'category', 'questionnaire_score', 
            'subcategory_scores'
            )


class QuestionnaireScoreNestedSerializer(serializers.ModelSerializer):
    """Nested serializer for uploading QuestionnaireScores from mobile"""
    category_scores = CategoryScoreNestedSerializer(many=True)

    class Meta:
        model = QuestionnaireScore
        depth = 5

    def create(self, validated_data):
        categories_data = validated_data.pop('category_scores')
        qnaire_score = QuestionnaireScore.objects.create(**validated_data)

        for category_data in categories_data:
            subcategories_data = category_data.pop('subcategory_scores')
            category_data.pop('questionnaire_score')
            category_score = CategoryScore.objects.create(questionnaire_score=qnaire_score, **category_data)

            for subcategory_data in subcategories_data:
                questions_data = subcategory_data.pop('question_scores')
                subcategory_data.pop('category_score')
                subcategory_score = SubcategoryScore.objects.create(category_score=category_score, **subcategory_data)

                for question_data in questions_data:
                    answers_data = question_data.pop('answer_scores')
                    question_answer_data = question_data.pop('answer')
                    question_data.pop('subcategory_score')
                    question_score = QuestionScore.objects.create(subcategory_score=subcategory_score, **question_data)

                    for answer_data in answers_data:
                        answer_data.pop('question_score')
                        AnswerScore.objects.create(question_score=question_score, **answer_data)

                    question_score.answer = AnswerScore.objects.get(question_score=question_score, answer=question_answer_data.answer)
                    question_score.save()

        return qnaire_score


#Definitions
class DefinitionSerializer(serializers.ModelSerializer):
    """Prepare Definitons for JSON"""
    class Meta:
        model= Definition
        fields = ("id", "display_word_text", "display_definition_text")

