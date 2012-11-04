import json
import functools

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template

from lstory.models import Story

from lqa.forms import QuestionCreateForm
from lqa.models import Question

from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form

def _ensure_user_and_story(function):
    @functools.wraps(function)
    def decorator(request, story_slug, *args, **kwargs):
        if not request.user.is_authenticated():
            return JSONResponse({'error': 'not authenticated'})

        stories = Story.objects.filter(slug=story_slug)

        if not stories:
            return JSONResponse({'error': 'story not found'})

        story = stories[0]

        return function(request, story, *args, **kwargs)
    return decorator



class JSONResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        kwargs['mimetype'] = 'application/json'
        super(JSONResponse, self).__init__(json.dumps(data), *args, **kwargs)

@_ensure_user_and_story
def create_question(request, story):
    f = QuestionCreateForm(request.POST)
    if f.is_valid():
        o = f.save(commit=False)
        o.story = story
        o.user = request.user
        o.save()
        return JSONResponse({'result': render_to_string('lqa/_question.html', {'question': o})})
    else:
        return JSONResponse({'form': as_crispy_form(f)})

@_ensure_user_and_story
def edit_question(request, story, question_id):
    q = Question.objects.get(id=question_id)
    f = QuestionCreateForm(request.POST, instance=q)
    if f.is_valid():
        o = f.save(commit=False)
        o.story = story
        o.user = request.user
        o.save()
        return JSONResponse({'result': render_to_string('lqa/_question.html', {'question': o})})
    else:
        return JSONResponse({'form': as_crispy_form(f)})

def show_question(request, story_slug, object_id):
    return direct_to_template(request, 'lqa/question.html', {'story': Story.objects.get(slug=story_slug), 'question': Question.objects.get(pk=object_id)})
