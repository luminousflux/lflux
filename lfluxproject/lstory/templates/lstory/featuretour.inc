{% load i18n %}
<li data-id="history" data-button="{% trans "Next" %}">
    <p>{% trans "The main text always represents our current understanding of the situation. When something happens, we try to update it daily." %}</p>
</li>
<li data-id="timelineversionbtn" data-button="{% trans "Next" %}">
    <p>{% trans "To make this process transparent, you can browse through all previous versions here." %}</p>
</li>

{% if previous %}<li data-id="versionlinkbtn" data-button="{% trans "Next" %}">
    <p>{% trans "If you want to link to the current version, or embed this story in your website, look here." %}</p>
</li>{% endif %}

<li data-id="timelinehighlightbtn" data-button="{% trans "Next" %}">
    <p>{% trans "Here you can see what changed between a previous version and now." %}</p>
</li>

<li data-id="sidebar" data-button="{% if current.backgroundcontent_set.all %}{% trans "Next" %}{% else %}{% trans "Close" %}{% endif %}">
    <p>{% trans "The 'Current Events' section is a collection of links relevant to the topic" %}
</li>

{% if current.backgroundcontent_set.all %}
<li data-id="backgroundcontentbtn" data-button="{% trans "Close" %}">
    <p>{% trans "Sometimes we interview people or publish background research. You can find these here." %}
</li>
{% endif %}


