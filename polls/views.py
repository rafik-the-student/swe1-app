from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"  # default: question_list

    def get_queryset(self):
        """return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    # default: <app name>/<model name>_detail.html
    # default: polls/question_detail.html
    template_name = "polls/detail.html"
    # context_object_name = 'question'  # default


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    # context_object_name = 'question'  # default


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form.
        context = {"question": question, "error_message": "You didn't select a choice."}
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # return a redirect
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
