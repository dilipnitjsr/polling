from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question,Choice
from django.shortcuts import get_object_or_404, render
from django import forms
from .forms import AddQuestionForm
from django.http import JsonResponse
from . import randomvoting

# Create your views here.

#def index(request):
	# latestQuestionList=Question.objects.order_by('-pub_date')
	# template=loader.get_template('polls/index.html')
	# context={'latest_question_list':latestQuestionList}
	# return HttpResponse(template.render(context,request))

class IndexView(generic.ListView):
	template_name='polls/index.html'
	context_object_name='latest_question_list'

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')

# def detail(request,question_id):
# 	try:
# 		question=Question.objects.get(pk=question_id)
# 	except Question.DoesNotExist:
# 		raise Http404('Question does not exists')
# 	return HttpResponse(loader.get_template('polls/detail.html').render({'question':question},request))

class DetailView(generic.DetailView):
	model=Question
	template_name='polls/detail.html'

# def results(request,question_id):
# 	try:
# 		question=Question.objects.get(pk=question_id)
# 	except Question.DoesNotExist:
# 		raise Http404('Question does not exists')
# 	return HttpResponse(loader.get_template('polls/results.html').render({'question':question},request))

class ResultsView(generic.DetailView):
	model=Question
	template_name='polls/results.html'

def vote(request,question_id):
	#randomvoting.testfunc(repeat=10)
	question=get_object_or_404(Question,pk=question_id)
	#print('vote, question = ',question)
	try:
		selected_choice=question.choice_set.get(pk=request.POST['choice'])
	except (KeyError,Choice.DoesNotExist):
		#print('choice does not exist')
		return render(request,'polls/detail.html',{'question':question,'error_message':'No choice selected'})
	else:
		selected_choice.votes+=1
		selected_choice.save()
	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def newQuestion(request):
	if request.method=='POST':
		form=AddQuestionForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			q=Question(question_text=form.cleaned_data['question_text'])
			q.save()
			for i in range(1,6):
				content=form.cleaned_data['choice'+i.__str__()].strip()
				if content:
					q.choice_set.create(choice_text=content,votes=0)
			return redirect('polls:index')
	else:
		form=AddQuestionForm()
		return render(request,'polls/newq.html',{'addQuestionForm':form})

def votesApi(request):
	question_id=request.GET['question_id']
	q=Question.objects.get(pk=question_id)
	#print('vote api returned question ',q)
	data={'question_text':q.question_text,'choices':[]}

	for c in q.choice_set.all():
		data['choices'].append({'choice_text':c.choice_text,'votes':c.votes})

	#print('data for JsonResponse = ',data)
	return JsonResponse(data)