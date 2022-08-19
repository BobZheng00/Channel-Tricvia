from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import json


# Create your models here.


class QuestionsSet(models.Model):
    type = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    question = models.TextField()
    correct_answer = models.CharField(max_length=200)
    incorrect_answer = ArrayField(models.CharField(max_length=200, null=True, blank=True), null=True,
                                  blank=True)

    @staticmethod
    def load_data():
        with open('C:/Users/23116/Trivial-Questions/questions_data.json') as json_file:
            data = json.load(json_file)
        for question in data['questions']:
            QuestionsSet.objects.create(type='question', category=str(question['category']),
                                        question=str(question['question']),
                                        correct_answer=str(question["correct answer"]), incorrect_answer=None)


class QuickTriviaLeaderboard(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    attempt = models.IntegerField(default=10)
    category = models.CharField(max_length=100)
    completed = models.DateTimeField(null=True, blank=True)


