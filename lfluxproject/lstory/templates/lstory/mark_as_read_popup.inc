{% load url from future %}{% load i18n %}

    {% if tracking_allowed %}
    {% trans "Next time you come here, we will highlight what changed since now." %}<br />
<div class="column-left">
    <span class="tracking-status reload-here" data-track="yes" data-track-url="{% url "mark_as_read" slug=current.versions.current.slug %}">
        {% trans "Marking as read" %}
    </span><br />
    <a href="{% url "disable_tracking" %}">
        {% trans "Disable this feature." %}
    </a>
    {% else %}
<div class="column-left">
    <span class="tracking-status reload-here" data-track="no">
        {% trans "Tracking disabled." %}
    </span><br />
    <a href="{% url "enable_tracking" %}">
        {% trans "Re-enable tracking." %}
    </a>
    {% endif %}
</div>
<div class="column-right">
    <a href="#help" id="featuretourbtn">{% trans "Learn more" %}</a><br />
    <a href="{% url 'lstory_subscribe' slug=current.versions.current.slug %}" class="ignorereload">{% trans "Sign up for updates" %}</a>
</div>
<div class="clear">&nbsp;</div>
