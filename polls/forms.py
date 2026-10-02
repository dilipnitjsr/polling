from django import forms


class AddQuestionForm(forms.Form):
    question_text = forms.CharField(label="Question", max_length=200)
    choice1 = forms.CharField(label="Choice 1", max_length=200)
    choice2 = forms.CharField(label="Choice 2", max_length=200)
    choice3 = forms.CharField(label="Choice 3", max_length=200, required=False)
    choice4 = forms.CharField(label="Choice 4", max_length=200, required=False)
    choice5 = forms.CharField(label="Choice 5", max_length=200, required=False)

    def clean(self):
        cleaned = super().clean()
        choices = [
            (cleaned.get(f"choice{i}") or "").strip()
            for i in range(1, 6)
        ]
        if len([choice for choice in choices if choice]) < 2:
            raise forms.ValidationError("At least two choices are required.")
        return cleaned
