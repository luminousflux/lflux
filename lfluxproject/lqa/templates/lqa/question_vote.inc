{% load url from future %}
{% load voting_tags static i18n %}
{% score_for_object question as score %}
{% vote_by_user request.user on question as vote %}
<div class="votecontainer">
    <div class="votes">
        <h2>{{score.score|default:'0'}}</h2>
        {% trans "votes" %}
    </div>
    <div class="vote" style="">
      <form class="questionvote" id="questionup{{ question.id }}" action="{% if vote and vote.is_upvote %}{% url 'lqa_question_vote' object_id=question.id direction='clear' %}{% else %}{% url 'lqa_question_vote' object_id=question.id direction='up' %}{% endif %}" method="POST">{% csrf_token %}
      <input type="image" id="questionuparrow{{ question.id }}" src="{% if vote and vote.is_upvote %}{% static 'img/arrow_up.png' %}{% else %}{% static 'img/arrow_up_grey.png' %}{% endif %}" {% if request.user.is_anonymous %}title="{% trans "Only works if you're logged in!" %}" disabled="disabled" {% endif %} />
      </form>
      <form class="questionvote" id="questiondown{{ question.id }}" action="{% if vote and vote.is_downvote %}{% url 'lqa_question_vote' object_id=question.id direction='clear' %}{% else %}{% url 'lqa_question_vote' object_id=question.id direction='down' %}{% endif %}" method="POST">{% csrf_token %}
        <input type="image" id="questiondownarrow{{ question.id }}" src="{% if vote and vote.is_downvote %}{% static 'img/arrow_down.png' %}{% else %}{% static 'img/arrow_down_grey.png' %}{% endif %}" {% if request.user.is_anonymous %}title="{% trans "Only works if you're logged in!" %}" disabled="disabled" {% endif %}>
      </form>
    </div>
</div>
