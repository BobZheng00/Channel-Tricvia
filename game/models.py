from django.db import models
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
