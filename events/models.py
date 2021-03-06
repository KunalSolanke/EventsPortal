from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model) :
    title = models.CharField(max_length=255,blank=False,null=True,unique=True)
    description = models.TextField(blank=True,null=True)
    min_per_team = models.IntegerField(null=True)
    max_per_team = models.IntegerField(null=True)
    

class SubTeam(models.Model) :
    event = models.ForeignKey(Event, related_name="teams_particiaptd", on_delete=models.CASCADE)
    team = models.ForeignKey("accounts.Team", related_name="subteams", on_delete=models.CASCADE)
    members = models.ManyToManyField("accounts.Profile", related_name="subteams")
    is_approved = models.BooleanField(default=False)
    submission_done = models.BooleanField(default=False)
    submission_link = models.URLField(blank=True,null=True)
    title = models.CharField(max_length=255,blank=False,null=True)
    description = models.TextField(blank=True,null=True)
