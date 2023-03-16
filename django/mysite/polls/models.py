import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
class Hub(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    address = models.GenericIPAddressField(default="0.0.0.0")
    port = models.IntegerField(default=0000)
    def __str__(self):
        return self.name
    
class Node(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    address = models.IntegerField(default=8)
    location = models.CharField(max_length=200)

class Data(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    temperature = models.FloatField(default=0.00)
    humidity = models.FloatField(default=0.00)
    pub_date = models.DateTimeField(auto_now_add=True)
    def is_most_recent(self):
        return

    
