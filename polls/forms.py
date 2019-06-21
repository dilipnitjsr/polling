from django import forms

class AddQuestionForm(forms.Form):
	question_text=forms.CharField(label='Question',max_length=100)

	choice1=forms.CharField(label='Choice 1:',max_length=100)
	choice2=forms.CharField(label='Choice 2:',max_length=100)
	choice3=forms.CharField(label='Choice 3:',max_length=100)
	choice4=forms.CharField(label='Choice 4:',max_length=100)
	choice5=forms.CharField(label='Choice 5:',max_length=100)

	def __init__(self,*args,**kwargs):
		super(AddQuestionForm,self).__init__(*args,**kwargs)
		for i in range(1,6):
			self.fields['choice'+i.__str__()].required=False