from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_api import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^questionnaire/$', views.QuestionnaireList.as_view(), name='questionnaire-list'),
    url(r'^questionnaire/(?P<pk>[0-9]+)/$', views.QuestionnaireDetail.as_view(), name='questionnaire-detail'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryDetail.as_view(), name='category-detail'),
    url(r'^question/(?P<pk>[0-9]+)/$', views.QuestionDetail.as_view(), name='question-detail'),
    url(r'^answer/(?P<pk>[0-9]+)/$', views.AnswerDetail.as_view(), name='answer-detail'),
])
