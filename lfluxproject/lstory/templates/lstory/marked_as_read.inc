{% load url from future %}
{% trans "Marked as read." %} {% if previous_value %}<a href='{% url "mark_as_read" slug=current.slug %}?to_value={{previous_value}}'>{% trans "Undo" %}</a>{% endif %}
