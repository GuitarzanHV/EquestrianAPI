from django.db import models

# Create your models here.
class Question(models.Model):
    """docstring for Question"""
    question_text = models.CharField(max_length=255)
    question_image = models.CharField(max_length=255)
    categories = models.ManyToMany(Category)

class Answer(models.Model):
    """docstring for Answer"""
    answer_text = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question)

class Category(models.Model):
    """docstring for Category"""
    category_name = models.CharField(max_length=255)
    questionnaires = models.ManyToMany(Questionnaire)

class Questionnaire(models.Model):
    """docstring for Questionnaire"""
    questionnaire_name = models.CharField(max_length=255)
