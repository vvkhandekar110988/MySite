from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
# from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


# Create your views here.


# def index(request):
# order first 5 questions in reverse order means recent 5 questions
# latest_question_list = Question.objects.order_by('-pub_date')[:5]

# , means join all questions by comma and for loop will give five questions and stored in output separated by comma
# output = ', '.join([q.question_text for q in latest_question_list])

# loading polls/index.html in template
# template = loader.get_template('polls/index.html')

# context is a dictionary with name key value
# context = {
# 'latest_question_list': latest_question_list
# }

# pass context value through template to the polls/index.html
# return HttpResponse(template.render(context, request))

# It will do exactly as 'return HttpResponse' have done
# return render(request, 'polls/index.html', context)


# def detail(request, question_id):
# try:
# app.com/polls/2 in browser then 2 will pass as question_id as primary key and will store primary key object
# information in question
# question = Question.objects.get(pk=question_id)
# question = get_object_or_404(Question, pk=question_id)
# if primary key is not exists then except bolck will execute
# except Question.DoesNotExist:
# raise Http404("Question does not exist")
# return HttpResponse("You are looking for questions %s." % question_id)
# return question object, polls/index.html
# return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
# question = get_object_or_404(Question, pk=question_id)
# return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        """
            Return the last five published questions (not including those set to be
            published in the future).
            """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
