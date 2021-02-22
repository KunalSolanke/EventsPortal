from django.shortcuts import render
from django.views.generic import ListView,DetailView,UpdateView,CreateView
from django.views import View
from .models import Event,SubTeam
from django.utils import timezone
from django.shortcuts import get_object_or_404


class EventsRegisterListView(ListView) :
    template_name = "events/register_list.html"
    model = Event
    
    def get_queryset(self) :
        queryset = Event.objects.filter(registration_starts__lte = timezone.now().date()).exclude(teams__in=[self.request.user.profile.team]).all()
        return queryset
    
    def get_context_data(self) :
        context = super(EventsRegisterListView,self).get_context_data(**kwargs)
        context["upcoming"] =Event.objects.filter(registration_starts__gte = timezone.now().date()).exclude(teams__in=[self.request.user.profile.team]).all()
        return context

class EventRegisterView(DetailView) :
      model = Event
      template_name = "events/register_teams.html"
      
      def get_context_data(self, **kwargs):
          context = super(EventRegisterView, self).get_context_data(**kwargs)
          context["subteams"] = SubTeam.objects.filter(team=self.request.user.profile.team,event__id=kwargs["pk"])
          return context

class AddSubTeamView(CreateView) :
    model = SubTeam
    fields  = ["members","name"]
    template_name = "events/add_subteam.html"
    
    def get_success_url(self) :
        return "/events/register/"+self.object.event.id

    def get_context_data(self) :
        context = super(AddSubmission),self).get_context_data(**kwargs)
        context["available_members"] = self.request.user.team.menbers.exclude(subteams__event__id=self.kwargs["pk"])
        context["event"] = get_object_or_404(Events,pk=team.event.pk)
        return context

class EventsSubmissionListView(ListView) :
    template_name = "events/submission_list.html"
    model = Event
    
    def get_queryset(self) :
        user = self.request.user
        queryset = Event.objects.filter(submission_starts__lte= timezone.now().date(),submission_ends__gte=timezone.now().date(),teams__in=[user.team]).all()
        return queryset
    
    def get_context_data(self) :
        context = super(EventsSubmissionListView,self).get_context_data(**kwargs)
        context["upcoming"] =Event.objects.filter(submission_starts__gte = timezone.now().date(),teams__in=[user.team]).all()
        context["submitted"] = self.request.profile.team.subteams.fiter(submission_done=True).all()
        return context

class EventSubmisionView(DetailView) :
      model = Event
      template_name = "events/submission_detail.html"
      
      def get_context_data(self, **kwargs):
          context = super(EventSubmisionView, self).get_context_data(**kwargs)
          context["subteams"] = SubTeam.objects.filter(team=self.request.user.team,event__id=kwargs["pk"])
          return context

class AddSubmission(UpdateView) :
    model = SubTeam
    fields  = ["description","submission_link","title","name"]
    template_name = "events/add_submission"
    
    def get_success_url(self) :
        return "/events/submission/"+self.object.event.id

    def get_context_data(self) :
        context = super(AddSubmission),self).get_context_data(**kwargs)
        team= self.object
        context["event"] = get_object_or_404(Events,pk=team.event.pk)
        return context

class RegisteredEventsView(ListView) :
    template_name = "events/registered_list.html"
    model = Event
    
    def get_queryset(self) :
        queryset = Event.objects.filter(teams__in=[self.request.user.profile.team]).all()
        return queryset


class SubmittedEventsView(ListView) :
    template_name = "events/submitted_list.html"
    model = Event
    
    def get_queryset(self) :
        queryset = self.request.profile.team.subteams.fiter(submission_done=True).all()
        return queryset