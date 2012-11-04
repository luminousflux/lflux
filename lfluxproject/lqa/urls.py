from django.conf.urls.defaults import patterns, include, url
from django.views.generic.list_detail import object_list
from voting.views import vote_on_object
from lqa.views import create_question, show_question
from lqa.models import Question

urlpatterns = patterns(
    '',
    url(r'^(?P<story_slug>[^/]*)/questions/create/$', create_question, name='lqa_question_create'),
    url(r'^(?P<story_slug>[^/]*)/questions/(?P<object_id>[^/]*)/$', show_question, name='lqa_question'),
    # Generic view to vote on Link objects
    url(r'^api/questions/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/$',
        vote_on_object, dict(model=Question, template_object_name='question',
            allow_xmlhttprequest=True), name='lqa_question_vote'),
)
