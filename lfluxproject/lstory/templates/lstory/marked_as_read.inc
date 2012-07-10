{% load url from future %}
Marked as read. {% if previous_value %}<a href='{% url "mark_as_read" slug=current.slug %}?to_value={{previous_value}}'>Undo</a>{% endif %}
