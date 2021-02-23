from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,UpdateView,CreateView
from django.views import View
from .models import Event,SubTeam
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class EventsRegisterListView(ListView) :
    template_name = "events/register_list.html"
    model = Event
    
    def get_queryset(self) :
        queryset = Event.objects.filter(registration_starts__lte = timezone.now().date()).exclude(teams__in=[self.request.user.profile.team]).all()
        return queryset
    
    def get_context_data(self,**kwargs) :
        context = super(EventsRegisterListView,self).get_context_data(**kwargs)
        context["upcoming"] =Event.objects.filter(registration_starts__gte = timezone.now().date()).exclude(teams__in=[self.request.user.profile.team]).all()
        return context

class EventRegisterView(DetailView) :
      model = Event
      template_name = "events/register_teams.html"
      
      def get_context_data(self, **kwargs):
          context = super(EventRegisterView, self).get_context_data(**kwargs)
          context["subteams"] = SubTeam.objects.filter(team=self.request.user.profile.team,event__id=kwargs["object"].id)
          context["event"]=kwargs["object"]
          return context

class AddSubTeamView(CreateView) :
    model=SubTeam
    fields=["title","members"]
    template_name = "events/add_subteam.html"

    def get_context_data(self, **kwargs) :
        context = super(AddSubTeamView,self).get_context_data(**kwargs)
        print(kwargs)
        context["available_members"] = self.request.user.team.members.exclude(subteams__event__id=self.kwargs["pk"])
        context["event"] = get_object_or_404(Event,pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs) :
        title= request.POST.get("title",None)
        members = request.POST.get("members",None)
        print(members)
        description = request.POST.get("memebers",None)
        event = get_object_or_404(Event,pk=kwargs["pk"])
        team = request.user.team
        team = SubTeam.objects.create(title=title,description=description,event=event,team=request.user.team)
        for id in members :
            user = get_object_or_404(User,pk=int(id))
            team.members.add(user.profile)
        team.save()
        return redirect("/events/register/"+str(kwargs["pk"]))

class EventsSubmissionListView(ListView) :
    template_name = "events/submission_list.html"
    model = Event
    
    def get_queryset(self) :
        user = self.request.user
        queryset = Event.objects.filter(submission_starts__lte= timezone.now().date(),submission_ends__gte=timezone.now().date(),teams__in=[user.team]).all()
        return queryset
    
    def get_context_data(self, **kwargs) :
        context = super(EventsSubmissionListView,self).get_context_data(**kwargs)
        user = self.request.user
        context["upcoming"] =Event.objects.filter(submission_starts__gte = timezone.now().date(),teams__in=[user.team]).all()
        context["submitted"] = user.profile.team.subteams.fiter(submission_done=True).all() if user.profile.team is not None else []
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

    def get_context_data(self,**kwargs) :
        context = super(AddSubmission,self).get_context_data(**kwargs)
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
        queryset = self.request.user.profile.team.subteams.fiter(submission_done=True).all()
        return queryset