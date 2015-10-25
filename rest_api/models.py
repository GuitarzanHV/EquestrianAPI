from django.db import models
from django.db.models import Sum

class Questionnaire(models.Model):
    """Lists the categories for each questionnaire type, as
    well as the maximum composite score for each score type
    """
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
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
    image = models.FilePathField(path='/var/www/images', default="", blank=True)
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
    owner = models.CharField(max_length=60)
    date_started = models.DateField(auto_now_add=True)
    date_last_edited = models.DateField(auto_now=True)
    questionnaire = models.ForeignKey(Questionnaire, related_name='+') #no backwards relation

    def score(self):
        for cat_score in self.category_scores.all():
            total = cat_score.score()

        return total

    def evaluation(self):
        qnaire_score = self.score()

        if qnaire_score > self.questionnaire.needs_work_score:
            return "Unacceptable"

        if qnaire_score > self.questionnaire.acceptable_score:
            return "Needs Work"

        return "Acceptable"

    def __str__(self):
        return self.name + ' ' + str(self.id)

class CategoryScore(models.Model):
    """Stores category scores, related to one QuestionnaireScore.
    """
    category = models.ForeignKey(Category, related_name='+')
    questionnaire_score = models.ForeignKey(QuestionnaireScore, related_name='category_scores')

    def score(self):
        return self.question_scores.aggregate(score=Sum('score'))['score']

    def evaluation(self):
        cat_score = self.score()

        if cat_score > self.category.needs_work_score:
            return "Unacceptable"

        if cat_score > self.category.acceptable_score:
            return "Needs Work"

        return "Acceptable"

    def __str__(self):
        return str(self.questionnaire_score) + ' ' + self.category.name

class QuestionScore(models.Model):
    """Stores question scores, as well as chosen answer.
    """
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='+')
    answer = models.ForeignKey(Answer, related_name='+', blank=True, null=True)
    category_score = models.ForeignKey(CategoryScore, related_name='question_scores')

    def __str__(self):
        return str(self.category_score) + ' ' + self.question.name
