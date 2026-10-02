from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text or ""


class SiteUser(models.Model):
    user_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name


class VotedOn(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "question"],
                name="one_vote_per_user_per_question",
            )
        ]
