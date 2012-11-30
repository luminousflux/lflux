{% load i18n %}
{% load markup humanize_timesince %}
{% load threadedcomments_tags %}
<div class="meta1">
    <span class="username">{{user}}</span>
    <span class="timeago">{{comment.submit_date|humanize_timesince}}</span>
</div>
{{ comment.comment|markdown }}
<div class="meta">
    <a href="#" onclick="$('#comment_form_for_{{comment.pk}}').toggle(); return false;">{% trans "reply" %}</a>
</div>

<div id="comment_form_for_{{comment.pk}}" style="display: none;">
    {% render_comment_form for comment.content_object with comment.pk %}
</div>

