from django.db import models
from django.db.models import Sum
from django.core.exceptions import FieldError


class Questionnaire(models.Model):
    """Lists the categories for each questionnaire type, as
    well as the maximum composite score for each score type
    """
    WESTERN = 'west'
    ENGLISH = 'engl'
    RIDING_STYLE_CHOICES = (
        (WESTERN, 'Western'),
        (ENGLISH, 'English')
    )

    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    mobile = models.BooleanField(default=True)
    riding_style = models.CharField(max_length=4, choices=RIDING_STYLE_CHOICES)
    acceptable_score = models.IntegerField(default=0)
    needs_work_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Holds the subcategories for each scored category, as well
    as maximum score for each score type. Many to Many 
    relationships with Subcategory and Questionnaire.
    """
    
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    acceptable_score = models.IntegerField(default=0)
    needs_work_score = models.IntegerField(default=0)
    questionnaires = models.ManyToManyField(Questionnaire, related_name='categories')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Subcategorizes questions in each category, such as walk and 
    trot in Gaits. Many to Many relationship with Category, many to one
    with Question.
    """
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='subcategories')

    def __str__(self):
        return self.name


class Question(models.Model):
    """Holds the text of a question, along with an image
    that goes with the question. Multiple Answers for each
    Question, Questions can be in more than one Category
    """
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    #image = models.FilePathField(path='/var/www/images', default="", blank=True)
    subcategory = models.ForeignKey(Subcategory, related_name='questions')

    def __str__(self):
        return self.name


class Answer(models.Model):
    """Text and numeric score for an Answer to a 
    Question. Each Answer only has one Question.
    """
    display_text = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')

    def __str__(self):
        return self.display_text


class QuestionnaireScore(models.Model):
    """Holds score categories for each individual questionnaire.
    Also holds horse names, horse owner, and dates started and edited.
    """
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    mobile = models.BooleanField(default=True)
    riding_style = models.CharField(max_length=4)
    acceptable_score = models.IntegerField(default=0)
    needs_work_score = models.IntegerField(default=0)
    horse_name = models.CharField(max_length=20)
    horse_owner = models.CharField(max_length=60)
    location = models.CharField(max_length=100)
    #owner = models.ForeignKey('auth.User', related_name='questionnaire_scores')
    date_started = models.DateField(auto_now_add=True)
    date_last_edited = models.DateField(auto_now=True)
    questionnaire = models.ForeignKey(Questionnaire, related_name='+', null=True) #no backwards relation

    def score(self):
        total = 0

        for cat in self.category_scores.all():
            total += cat.score()

        return total

    def evaluation(self):
        qnaire_score = self.score()

        if qnaire_score > self.needs_work_score:
            return "Unacceptable"

        if qnaire_score > self.acceptable_score:
            return "Needs Work"

        return "Acceptable"

    def __str__(self):
        return ' '.join((str(self.id), self.name, self.horse_name))


class CategoryScore(models.Model):
    """Stores category scores, related to one QuestionnaireScore."""
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    acceptable_score = models.IntegerField(default=0)
    needs_work_score = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='+', null=True)
    questionnaire_score = models.ForeignKey(QuestionnaireScore, related_name='category_scores')

    def score(self):
        total = 0

        for subcat in self.subcategory_scores.all():
            try:
                total += subcat.question_scores.aggregate(score=Sum('answer.score'))['score']
            except FieldError:
                total += 0

        return total

    def evaluation(self):
        cat_score = self.score()

        if cat_score > self.needs_work_score:
            return "Unacceptable"

        if cat_score > self.acceptable_score:
            return "Needs Work"

        return "Acceptable"

    def __str__(self):
        return ' '.join((str(self.questionnaire_score), self.category.name))


class SubcategoryScore(models.Model):
    """Stores an instance of a subcategory for scoring."""
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    subcategory = models.ForeignKey(Subcategory, related_name='+', null=True)
    category_score = models.ForeignKey(CategoryScore, related_name='subcategory_scores')

    def __str__(self):
        return ' '.join((str(self.category_score), self.subcategory.name))


class QuestionScore(models.Model):
    """Stores question scores, as well as chosen answer."""
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    #image = models.FilePathField(path='/var/www/images', default="", blank=True)
    question = models.ForeignKey(Question, related_name='+', null=True)
    answer = models.ForeignKey('AnswerScore', related_name='+', blank=True, null=True)
    subcategory_score = models.ForeignKey(SubcategoryScore, related_name='question_scores')

    def __str__(self):
        return ' '.join((str(self.subcategory_score), self.question.name))


class AnswerScore(models.Model):
    """Stores instance of an answer for scoring"""
    display_text = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    answer = models.ForeignKey(Answer, related_name='+', null=True)
    question_score = models.ForeignKey(QuestionScore, related_name='answer_scores')

    def __str__(self):
        return ' '.join((str(self.question_score), str(self.answer.score)))


class Definition(models.Model):
    """Stores the definitions for the glossary section."""
    display_word_text = models.CharField(max_length=20)
    display_definition_text = models.CharField(max_length=600)

    def __str__(self):
        return self.display_word_text

