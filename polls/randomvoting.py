from background_task import background
from .models import Question,Choice
import random

@background(schedule=0)
def testfunc():
	print('background scheduler test..3')
	#print(dir(Question))
	for q in Question.objects.all():
		print(q)
		choices=q.choice_set.all()
		n=random.randint(1,len(choices))
		print('question = ',q,' n = ',n)
		print(choices)
		try:
			ch=q.choice_set.get(pk=n)
			print('choice selected = ',ch)
			ch.votes+=1
			ch.save()
			q.save()
		except:
			pass
		#selected_choice=q.choice_set.get(pk=n)
		#selected_choice.votes+=1
		#print(len(q.choice_set.all()))
		#choices[n].votes+=1
		# i=1
		# for c in choices:
		# 	if i==n:
		# 		c.votes+=1
		# 	i+=1

		#q.save()

