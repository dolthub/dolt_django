import datetime

from django.db import models, connection
from django.utils import timezone
from django.contrib import admin

def _dolt_commit(message):
    with connection.cursor() as cursor:
        cursor.execute("CALL DOLT_COMMIT('-Am', '" + message + "')")

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)

        _dolt_commit("Saved a question")        
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def save(self, *args, **kwargs):
        super(Choice, self).save(*args, **kwargs)

        _dolt_commit("Saved a choice")

