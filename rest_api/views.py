from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'questionnaires': reverse('questionnaire-list', request=request, format=format)
        #'questionnaire scores': reverse('questionnaire-score-list', request=request, format=format)
    })

class QuestionnaireList(generics.ListAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class QuestionnaireDetail(generics.RetrieveAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryDetail(generics.RetrieveAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerDetail(generics.RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class QuestionnaireScoreList(generics.ListCreateAPIView):
    queryset = QuestionnaireScore.objects.all()
    serializer_class =  QuestionnaireScoreSerializer

class QuestionnaireScoreDetail(generics.RetrieveUpdateAPIView):
    queryset = QuestionnaireScore.objects.all()
    serializer_class = QuestionnaireScoreSerializer

class CategoryScoreDetail(generics.RetrieveAPIView):
    queryset = QuestionnaireScore.objects.all()
    serializer_class = CategoryScoreSerializer

class QuestionScoreDetail(generics.RetrieveUpdateAPIView):
    queryset = QuestionScore.objects.all()
    serializer_class = QuestionScoreSerializer
