#from background_task import background
from .models import Question,Choice
import random

import time
#@background(schedule=0)
def testfunc():
	while (True):
		time.sleep(2)
		print('background scheduler test..3')
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
		