{% load i18n %}
{% load markup humanize_timesince %}
{% load threadedcomments_tags %}
{{ comment.comment|markdown }}
<div class="meta">
    <span class="username {% if question and question.story and comment.user in question.story.authors.all %}author{% endif %}">
        {{comment.user}}
        {% if question and question.story and comment.user in question.story.authors.all %}
            <span class="userlabel">{% trans "(Author)" %}</span>
        {% endif %}
    </span>
    <span class="timeago">{{comment.submit_date|humanize_timesince}}</span>
    <a href="#" onclick="$('#comment_form_for_{{comment.pk}}').toggle(); return false;">{% trans "reply" %}</a>
</div>

<div id="comment_form_for_{{comment.pk}}" style="display: none;">
    {% if request.user.is_authenticated %}
        {% render_comment_form for comment.content_object with comment.pk %}
    {% else %}
        <div class="pleaselogin">{% trans "Please log in to post a comment!"%}</div>
    {% endif %}
</div>

