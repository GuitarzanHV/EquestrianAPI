from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'questionnaires': reverse('questionnaire-list', request=request, format=format),
        'questionnaire scores': reverse('questionnairescore-list', request=request, format=format)
    })


class QuestionnaireList(generics.ListAPIView):
    "Lists all questionnaires in the database"
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class QuestionnaireDetail(generics.RetrieveAPIView):
    "Provides detail on one Questionnaire object"
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class CategoryDetail(generics.RetrieveAPIView):
    "Provides detail on one Category object, the second level of a questionnaire."
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryDetail(generics.RetrieveAPIView):
    "Provides detail of a Subcategory object. the third level of a questionnaire"
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class QuestionDetail(generics.RetrieveAPIView):
    "Provides detail on a Question object, the fourth level of a questionnaire"
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerDetail(generics.RetrieveAPIView):
    "Provides detail on an Answer object, the fifth level of a questionnaire"
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuestionnaireScoreList(generics.ListCreateAPIView):
    "Lists all scored questionnaires in the database"
    queryset = QuestionnaireScore.objects.all()
    serializer_class =  QuestionnaireScoreSerializer


class QuestionnaireScoreDetail(generics.RetrieveUpdateAPIView):
    "Provides detail on a single scored questionnaire"
    queryset = QuestionnaireScore.objects.all()
    serializer_class = QuestionnaireScoreSerializer


class QuestionnaireScoreNestedCreate(generics.CreateAPIView):
    """Create a QuestionnaireScore object and sub-objects with specified data.
    Useful for uploading a completed questionnaire.
    """
    queryset = QuestionnaireScore.objects.all()
    serializer_class = QuestionnaireScoreNestedSerializer


class QuestionnaireScoreNestedDetail(generics.RetrieveUpdateAPIView):
    """Able to update or retrieve a QuestionnaireScore and sub-objects all
    at once.
    """
    queryset = QuestionnaireScore.objects.all()
    serializer_class = QuestionnaireScoreNestedSerializer


class CategoryScoreDetail(generics.RetrieveAPIView):
    "Provides detail for a scored category of a questionnaire"
    queryset = CategoryScore.objects.all()
    serializer_class = CategoryScoreSerializer


class SubcategoryScoreDetail(generics.RetrieveAPIView):
    "Provides detail for a scored subcategory of a questionnaire"
    queryset = SubcategoryScore.objects.all()
    serializer_class = SubcategoryScoreSerializer


class QuestionScoreDetail(generics.RetrieveUpdateAPIView):
    "Provides detail for a scored question of a questionnaire"
    queryset = QuestionScore.objects.all()
    serializer_class = QuestionScoreSerializer


class AnswerScoreDetail(generics.RetrieveAPIView):
    "Allows a questionnaire to remember wording of answers at time of completion"
    queryset = AnswerScore.objects.all()
    serializer_class = AnswerScoreSerializer


class DefinitionDetail(generics.RetrieveAPIView):
    "Provides definitions of a word in the database"
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
