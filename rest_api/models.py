from django.db import models

# Create your models here.
class Questionnaire(models.Model):
    """Lists the categories for each questionnaire type, as
    well as the maximum composite score for each score type
    """
    questionnaire_name = models.CharField(max_length=255)
    acceptable_score = models.IntegerField(default=0)
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
    acceptable_score = models.IntegerField(default=0)
    needs_work_score = models.IntegerField(default=0)
    unacceptable_score = models.IntegerField(default=0)
    questionnaires = models.ManyToManyField(Questionnaire)

    def __str__(self):
        return self.category_name

class Question(models.Model):
    """Holds the text of a question, along with an image
    that goes with the question. Multiple Answers for each
    Question, Questions can be in more than one Category
    """
    question_text = models.CharField(max_length=255)
    question_image = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    """Text and numeric score for an Answer to a 
    Question. Each Answer only has one Question."""
    answer_text = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question)

    def __str__(self):
        return self.answer_text
