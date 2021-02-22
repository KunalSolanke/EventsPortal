from django.db import models

# Create your models here.

class Event(models.Model) :
    title = models.CharField(max_length=255,blank=False,null=False)
    description = models.TextField(blank=True,null=True)
    registration_starts = models.DateField(blank=True)
    registration_end = models.DateField(blank=True)
    submission_starts = models.DateField(blank=True)
    submission_ends = models.DateField(blank=True)
    max_members_per_team = models.IntegerField(null=True)
    teams = models.ManyToManyField("accounts.Teams",related_name="events_registered")
    
    class Meta :
        ordering = ('-registration_starts',)

class SubTeam(models.Model) :
    name = models.CharField(max_length=255,blank=False,null=False)
    event = models.ForeignKey(Event, related_name="teams", on_delete=models.CASCADE)
    team = models.ForeignKey("accounts.Team", related_name="subteams", on_delete=models.CASCADE)
    members = models.ManyToManyField("accounts.Profile", related_name="subteams")
    is_approved = models.BooleanField(default=False)
    submission_done = models.BooleanField(default=False)
    submission_link = models.URLField(blank=True,null=True)
    title = models.CharField(max_length=255,blank=False,null=False)
    description = models.TextField(blank=True,null=True)