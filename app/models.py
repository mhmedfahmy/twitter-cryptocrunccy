from django.db import models

class results(models.Model):
    coin = models.CharField(max_length=200)
    retweets = models.IntegerField()
    followers = models.IntegerField()
