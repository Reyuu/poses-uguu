from django.db import models

# Create your models here.

class Devs(models.Model):
    deviationid = models.CharField(max_length=64)
    content_src = models.TextField()
    url = models.TextField()
    published_time = models.IntegerField()
    is_mature = models.BooleanField()
    viewable = models.BooleanField(default=True)

class DoneDevs(models.Model):
    username = models.CharField(max_length=64)
    last_updated = models.IntegerField()
    last_published_date = models.IntegerField()

class ReportedPics(models.Model):
    deviationid = models.CharField(max_length=64)
    report_count = models.IntegerField()

class IgnoredPics(models.Model):
    deviationid = models.CharField(max_length=64)

class SuggestionBox(models.Model):
    username = models.CharField(max_length=64)
    suggest_count = models.IntegerField()
    done = models.BooleanField(default=False)

class FeedbackBox(models.Model):
    feedback = models.TextField()
    done = models.BooleanField(default=False)