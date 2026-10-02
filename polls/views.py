from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_GET, require_POST

from .forms import AddQuestionForm
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


@require_POST
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        choice_id = request.POST["choice"]
    except KeyError:
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "No choice selected"},
            status=400,
        )

    selected_choice = get_object_or_404(
        Choice,
        pk=choice_id,
        question=question,
    )
    Choice.objects.filter(pk=selected_choice.pk).update(votes=F("votes") + 1)

    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def newQuestion(request):
    if request.method == "POST":
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(
                question_text=form.cleaned_data["question_text"]
            )
            for i in range(1, 6):
                content = (form.cleaned_data.get(f"choice{i}") or "").strip()
                if content:
                    question.choice_set.create(choice_text=content)
            return redirect("polls:index")
    else:
        form = AddQuestionForm()

    return render(request, "polls/newq.html", {"addQuestionForm": form})


@require_GET
def votesApi(request):
    question_id = request.GET.get("question_id")
    if not question_id:
        return JsonResponse({"error": "question_id is required"}, status=400)

    question = get_object_or_404(Question, pk=question_id)
    data = {
        "question_text": question.question_text,
        "choices": [
            {"choice_text": choice.choice_text, "votes": choice.votes}
            for choice in question.choice_set.all()
        ],
    }
    return JsonResponse(data)
