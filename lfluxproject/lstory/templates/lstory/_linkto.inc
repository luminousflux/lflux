{% load i18n %}
<{{h|default:"h2"}}><a href="{{story.get_absolute_url}}">{{story.title}}</a>
<span class="author">{% trans "by" %} {% for u in story.authors.all %}{% if not u.get_full_name %}{{u.username}}{% else %}{{u.get_full_name}}{%endif%}{% if not forloop.last %}, {%endif%}{% endfor %}</span></{{h|default:"h2"}}>

