from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import FieldError

class Questionnaire(models.Model):
    """Lists the categories for each questionnaire type, as
    well as the maximum composite score for each score type
    """
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    mobile = models.BooleanField(default=True)
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
    acceptable_score = models.IntegerField(default=0)
    needs_work_score = models.IntegerField(default=0)
    horse_name = models.CharField(max_length=20)
    horse_owner = models.CharField(max_length=60)
    date_started = models.DateField(auto_now_add=True)
    date_last_edited = models.DateField(auto_now=True)
    questionnaire = models.ForeignKey(Questionnaire, related_name='+', null=True) #no backwards relation

    def get_score(self):
        total = 0

        for cat in self.category_scores.all():
            total += cat.get_score()

        return total

    def get_evaluation(self):
        qnaire_score = self.get_score()

        if qnaire_score > self.needs_work_score:
            return "Unacceptable"

        if qnaire_score > self.acceptable_score:
            return "Needs Work"

        return "Acceptable"

    def __str__(self):
        return str(self.id) + ' ' + self.name + ' ' + self.horse_name

class CategoryScore(models.Model):
    """Stores category scores, related to one QuestionnaireScore.
    """
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    acceptable_score = models.IntegerField(default=0)
    needs_work_score = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='+')
    questionnaire_score = models.ForeignKey(QuestionnaireScore, related_name='category_scores', null=True)

    def get_score(self):
        total = 0

        for subcat in self.subcategory_scores.all():
            try:
                total += subcat.question_scores.aggregate(score=Sum('answer.score'))['score']
            except FieldError:
                total += 0

        return total

    def get_evaluation(self):
        cat_score = self.get_score()

        if cat_score > self.needs_work_score:
            return "Unacceptable"

        if cat_score > self.acceptable_score:
            return "Needs Work"

        return "Acceptable"

    def __str__(self):
        return str(self.questionnaire_score) + ' ' + self.category.name

class SubcategoryScore(models.Model):
    """
    Stores an instance of a subcategory for scoring.
    """
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    subcategory = models.ForeignKey(Subcategory, related_name='+', null=True)
    category_score = models.ForeignKey(CategoryScore, related_name='subcategory_scores')

    def __str__(self):
        return str(self.category_score) + ' ' + self.subcategory.name

class QuestionScore(models.Model):
    """Stores question scores, as well as chosen answer.
    """
    name = models.CharField(max_length=20)
    display_text = models.CharField(max_length=100)
    #image = models.FilePathField(path='/var/www/images', default="", blank=True)
    question = models.ForeignKey(Question, related_name='+', null=True)
    answer = models.ForeignKey('AnswerScore', related_name='+', blank=True, null=True)
    subcategory_score = models.ForeignKey(SubcategoryScore, related_name='question_scores')

    def __str__(self):
        return str(self.subcategory_score) + ' ' + self.question.name

class AnswerScore(models.Model):
    """
    Stores instance of an answer for scoring
    """
    display_text = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    answer = models.ForeignKey(Answer, related_name='+', null=True)
    question_score = models.ForeignKey(QuestionScore, related_name='answer_scores')

    def __str__(self):
        return str(self.category_score) + ' ' + self.question.name


return str(self.question_score) + ' ' + str(self.answer.score)

@receiver(post_save, sender=QuestionnaireScore)
def create_questionnaire_copy(sender, instance=None, created=False, **kwargs):
    if created:
        instance.name = instance.questionnaire.name
        instance.display_text = instance.questionnaire.display_text
        instance.acceptable_score = instance.questionnaire.acceptable_score
        instance.needs_work_score = instance.questionnaire.needs_work_score

        for category in instance.questionnaire.categories.all():
            cat_score = CategoryScore(
                category=category,
                questionnaire_score=instance
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

class Definition(models.Model):

"""Stores the definitions for the glossary section. 
"""
    definition_id = models.IntegerField(default=0)
    display_word_text = models.charField(max_length=20)
    display_definition_text = models.CharField(max_length=600)

def __str__(self):
    return self.Definition

