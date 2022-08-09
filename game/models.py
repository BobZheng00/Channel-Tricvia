from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class QuestionsSet(models.Model):
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    question = models.TextField()
    correct_answer = models.CharField(max_length=100)
    incorrect_answer = ArrayField(models.CharField(max_length=100, null=True, blank=True), null=True,
                                           blank=True)

    def load_data(self):
        with open('C:/Users/23116/Trivial-Questions/questions_data.json') as json_file:
            data = json.load(json_file)
        for question in data['questions']:
            self.objects.create(type='question', category=str(question['category']), question=str(question['question']),
                                correct_answer=str(question["correct answer"]), incorrect_answer=None)
