from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0003_siteuser_votedon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="choice_text",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="choice",
            name="votes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="question",
            name="pub_date",
            field=models.DateTimeField(verbose_name="date published"),
        ),
        migrations.AddConstraint(
            model_name="votedon",
            constraint=models.UniqueConstraint(
                fields=("user", "question"),
                name="one_vote_per_user_per_question",
            ),
        ),
    ]
