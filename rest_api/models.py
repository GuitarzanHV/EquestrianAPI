from django.db import models

class Questionnaire(models.Model):
    """Lists the categories for each questionnaire type, as
    well as the maximum composite score for each score type
    """
    questionnaire_name = models.CharField(max_length=255)
    questionnaire_text = models.CharField(max_length=255)
    needs_work_score = models.IntegerField(default=0)
    unacceptable_score = models.IntegerField(default=0)

    def __str__(self):
        return self.questionnaire_name

class Category(models.Model):
    """Holds the questions for each scored category, as well
    as maximum score for each score type. Many to Many 
    relationships with Question and Questionnaire.
    """
    category_name = models.CharField(max_length=255)
    category_text = models.CharField(max_length=255)
    needs_work_score = models.IntegerField(default=0)
    unacceptable_score = models.IntegerField(default=0)
    questionnaires = models.ManyToManyField(Questionnaire, related_name='categories')

    def __str__(self):
        return self.category_name

class Question(models.Model):
    """Holds the text of a question, along with an image
    that goes with the question. Multiple Answers for each
    Question, Questions can be in more than one Category
    """
    question_name = models.CharField(max_length=255)
    question_text = models.CharField(max_length=255)
    question_image = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='questions')

    def __str__(self):
        return self.question_name

class Answer(models.Model):
    """Text and numeric score for an Answer to a 
    Question. Each Answer only has one Question.
    """
    answer_text = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')

    def __str__(self):
        return self.answer_text

class QuestionnaireScore(models.Model):
    """Holds score categories for each individual horse.
        Also holds horse names.
    """
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    date_started = models.DateField(auto_now_add=True)
    date_last_edited = models.DateField(auto_now=True)
    questionnaire = models.ForeignKey(Questionnaire, related_name='+') #no backwards relation

    def __str__(self):
        return self.pk

class CategoryScore(models.Model):
    """Stores category scores, related to one Horse.
    """
    category = models.ForeignKey(Category, related_name='+')
    questionnaire_score = models.ForeignKey(QuestionnaireScore, related_name='category_scores')

    def score():
        pass

    def __str__(self):
        return self.horse.pk + ' ' + self.category.category_name

class QuestionScore(models.Model):
    """Stores question scores, as well as chosen answer.
    """
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='+')
    answer = models.ForeignKey(Answer, related_name='+')
    category_score = models.ForeignKey(CategoryScore, related_name='question_scores')

    def __str__(self):
        return self.category_score + ' ' + self.question.question_name
