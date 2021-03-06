from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_api import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    # url(r'^user/$',
    #     views.UserList.as_view(),
    #     name='user-list'
    # ),
    # url(r'^user/?P<pk>[0-9]+/$',
    #     views.UserDetail.as_view(),
    #     name='user-detail'
    # ),
    url(r'^questionnaire/$', 
        views.QuestionnaireList.as_view(), 
        name='questionnaire-list'
    ),
    url(r'^questionnaire/(?P<pk>[0-9]+)/$', 
        views.QuestionnaireDetail.as_view(), 
        name='questionnaire-detail'
    ),
    url(r'^category/(?P<pk>[0-9]+)/$', 
        views.CategoryDetail.as_view(), 
        name='category-detail'
    ),
    url(r'^subcategory/(?P<pk>[0-9]+)/$',
        views.SubcategoryDetail.as_view(),
        name='subcategory-detail'
    ),
    url(r'^question/(?P<pk>[0-9]+)/$', 
        views.QuestionDetail.as_view(), 
        name='question-detail'
    ),
    url(r'^answer/(?P<pk>[0-9]+)/$', 
        views.AnswerDetail.as_view(), 
        name='answer-detail'
    ),
    url(r'^questionnaire_score/$',
        views.QuestionnaireScoreList.as_view(),
        name='questionnairescore-list'
    ),
    url(r'^questionnaire_score/(?P<pk>[0-9]+)/$',
        views.QuestionnaireScoreDetail.as_view(),
        name='questionnairescore-detail'
    ),
    url(r'^questionnaire_score_nested/$',
        views.QuestionnaireScoreNestedCreate.as_view(),
        name='questionnairescorenested-create'
    ),
    url(r'^questionnaire_score_nested/(?P<pk>[0-9]+)/$',
        views.QuestionnaireScoreNestedDetail.as_view(),
        name='questionnairescorenested-detail'
    ),
    url(r'^category_score/(?P<pk>[0-9]+)/$',
        views.CategoryScoreDetail.as_view(),
        name='categoryscore-detail'
    ),
    url(r'^subcategory_score/(?P<pk>[0-9]+)/$',
        views.SubcategoryScoreDetail.as_view(),
        name='subcategoryscore-detail'
    ),
    url(r'^question_score/(?P<pk>[0-9]+)/$',
        views.QuestionScoreDetail.as_view(),
        name='questionscore-detail'
    ),
    url(r'^answer_score/(?P<pk>[0-9]+)/$',
        views.AnswerScoreDetail.as_view(),
        name='answerscore-detail'
    ),
    url(r'^definition/(?P<pk>[0-9]+)/$',
        views.DefinitionDetail.as_view(),
        name='definition-detail'
    ),
])
