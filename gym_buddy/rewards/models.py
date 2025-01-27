from django.db import models

class Reward(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
