import datetime

from django.db import models
from django.utils import timezone
    
class Hub(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200, default="0.0.0.0")
    port = models.IntegerField(default=0000)
    def __str__(self):
        return self.name
    def get_name(self):
        return f'{self.name}'
    def get_location(self):
        return f'{self.location}'
    
class Node(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    address = models.IntegerField(default=8)
    location = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default='')
    def __str__(self):
        return f'{self.hub}{self.address}'
    def get_name(self):
        return f'{self.name}'
    def get_address(self):
        return f'{self.address}'

class Data(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    temperature = models.FloatField(default=0.00)
    humidity = models.FloatField(default=0.00)
    pub_date = models.DateTimeField(auto_now_add=False, unique=True)
    def is_most_recent(self):
        return

    
