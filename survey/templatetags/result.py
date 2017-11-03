from django import template
from survey import models
register= template.Library()

@register.simple_tag
def average(question):
    score_type_results = question.surveyitemresult_set.all()
    score=[i.score for i in score_type_results]
    average = sum(score)/len(score)
    return round(average,2)


