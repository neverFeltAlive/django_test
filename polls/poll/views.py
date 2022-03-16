from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse

from .models import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    return render(request, 'poll/index.html', {
        'latest_question_list': latest_question_list,
        'title': 'Home',
    })


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'poll/detail.html', {
        'question': question,
        'title': 'Question: ' + question.question_text,
    })


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {
        'question': question,
    })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))
