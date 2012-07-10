{% load url from future %}
Looks like you're done reading!<br />
{% if tracking_allowed %}
<span class="tracking-status reload-here" data-track="yes" data-track-url="{% url "mark_as_read" slug=current.slug %}">Marking as read</span>
<a href="{% url "disable_tracking" %}">I don't want this feature, Disable tracking.</a>
{% else %}
<span class="tracking-status reload-here" data-track="no">You told us not to highlight what changed in stories since you last read them.</span><br />
<a href="{% url "enable_tracking" %}">Strike that, I'd like to know what changed. Enable tracking.</a>
{% endif %}

