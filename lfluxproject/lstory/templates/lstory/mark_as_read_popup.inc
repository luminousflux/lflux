{% load url from future %}
Looks like you're done reading!<br />
{% if tracking_allowed %}
We'll remember that you read it now and will highlight any changes when you next visit.<br />
<a href="{% url "disable_tracking" %}">I don't want this feature, Disable tracking.</a>
{% else %}
You told us not to highlight what changed in stories since you last read them.<br />
<a href="{% url "enable_tracking" %}">Strike that, I'd like to know what changed. Enable tracking.</a>
{% endif %}

