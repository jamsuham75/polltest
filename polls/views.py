from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Question, Choice
# Create your views here.
def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]   # order_by('속성명') : 오름차순, ('-속성명') : 내림차순
    # output = " ,".join([q.question_text for q in latest_question_list]) # 리스트를 문자열로 바꿔주고 " ,"로 원소 중간중간 넣어주겠다는 것.
    # return HttpResponse(output)

    latest_question_list = Question.objects.order_by('-pub_date')[:5]   # order_by('속성명') : 오름차순, ('-속성명') : 내림차순
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # return HttpResponse("Youre look at %s" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question
    }
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})

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
