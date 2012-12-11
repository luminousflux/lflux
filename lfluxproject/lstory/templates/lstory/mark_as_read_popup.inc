{% load url from future %}{% load i18n %}
{% trans "Looks like you're done reading!" %}<br />
{% if tracking_allowed %}
<span class="tracking-status reload-here" data-track="yes" data-track-url="{% url "mark_as_read" slug=current.versions.current.slug %}">{% trans "Marking as read" %}</span>
<a href="{% url "disable_tracking" %}">{% trans "I don't want this feature, Disable tracking." %}</a>
{% else %}
<span class="tracking-status reload-here" data-track="no">{% trans "You told us not to highlight what changed in stories since you last read them." %}</span><br />
<a href="{% url "enable_tracking" %}">{% trans "Strike that, I'd like to know what changed. Enable tracking." %}</a>
{% endif %}

