from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,UpdateView,CreateView
from django.views import View
from .models import Event,SubTeam
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from accounts.mixins import ProfileMixin
from accounts.models import Profile
from django.db import transaction
from django.db.models import Exists,OuterRef
from django.http import JsonResponse


def get_registered_events(user) :
    events = Event.objects.filter(teams_particiaptd__team__in=[user.team]).distinct()
    events_list =[]
    data ={}
    for event in events.all() :
        data["event"]=event
        data["subteams"]=user.team.subteams.filter(event__title=event.title)
        events_list+=[data]
        data={}

    return events_list

class EventRegisterView(ProfileMixin,View) :
      
      def get_context_data(self, **kwargs):
          context={}
          event,_ = Event.objects.get_or_create(title=kwargs["event_name"])
          context["subteams"] = SubTeam.objects.filter(team=self.request.user.team,event__title=kwargs["event_name"])
          context["event_name"] = kwargs["event_name"]
          context["registered_events"]=get_registered_events(self.request.user)
          return context
      
      def get(self,request,*args,**kwargs) :
          event_name=kwargs["event_name"]
          template_name="events/"+event_name+".html"
          return render(request,template_name,self.get_context_data(**kwargs))



class AddSubTeamView(ProfileMixin,View) :
    template_name = "events/add_subteam.html"

    def get(self,request,*args,**kwargs) :
        context={}
        context["available_members"] = []
        event,_ = Event.objects.get_or_create(title=kwargs["event_name"])
        context["team_members"] = self.request.user.team.members.all().annotate(is_registered = 
           Exists(
               SubTeam.objects.filter(members__id=OuterRef("id"),event__title=event.title)
           )
        )
        context["registered_events"]=get_registered_events(self.request.user)
        for member in self.request.user.team.members.exclude(subteams__event__title=event.title).all() :
            context["available_members"].append({
                "pk":member.pk,
                "name":member.fullname or member.first_name+" "+member.last_name
            })
        context["event_name"] = kwargs["event_name"]
        context["event"]=event
        return render(request,self.template_name,context=context)
    
    @transaction.atomic
    def post(self,request,*args,**kwargs) :
        event = get_object_or_404(Event,title=kwargs["event_name"])
        title= request.POST.get("title",None)
        members = request.POST.getlist("members",None)
        errors = {}
        
        description = request.POST.get("description",None)
        team = request.user.team
        team = SubTeam.objects.create(title=title,description=description,event=event,team=request.user.team)
        
        for id in members :
            if id=="" :
                continue
            user = get_object_or_404(Profile,pk=int(id))
            if user in team.members.all()  :
                raise Exception("Team member already in other subteam")
                return JsonResponse({"stat":400,"error":f"Member {user.first_name} {user.last_name} has already been added in other team"})
            team.members.add(user)
        team.save()
        return JsonResponse({"stat":200})
    


class AddSubmission(ProfileMixin,UpdateView) :
    model = SubTeam
    fields  = ["submission_link"]
    
    def get_success_url(self) :
        return self.request.META.get('HTTP_REFERER')

    def get_context_data(self,**kwargs) :
        context = super(AddSubmission,self).get_context_data(**kwargs)
        team= self.object
        context["event"] = get_object_or_404(Event,pk=team.event.pk)
        return context




"""
class RegisteredEventsView(ProfileMixin,ListView) :
    template_name = "events/registered_list.html"
    model = Event
    
    def get_queryset(self) :
        queryset = Event.objects.filter(teams__in=[self.request.user.profile.team]).all()
        return queryset


class SubmittedEventsView(ProfileMixin,ListView) :
    template_name = "events/submitted_list.html"
    model = Event
    
    def get_queryset(self) :
        queryset = self.request.user.profile.team.subteams.fiter(submission_done=True).all()
        return queryset


class EventsSubmissionListView(ProfileMixin,ListView) :
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
        context["submitted"] = user.profile.team.subteams.filter(submission_done=True).all() if user.profile.team is not None else []
        return context

class EventSubmisionView(ProfileMixin,DetailView) :
      model = Event
      template_name = "events/submission_detail.html"
      
      def get_context_data(self, **kwargs):
          context = super(EventSubmisionView, self).get_context_data(**kwargs)
          context["subteams"] = SubTeam.objects.filter(team=self.request.user.team,event__id=kwargs["pk"])
          return context


class EventsRegisterListView(ProfileMixin,ListView) :
    template_name = "events/register_list.html"
    model = Event
    
    def get_queryset(self) :
        queryset = Event.objects.filter(registration_starts__lte = timezone.now().date()).exclude(teams__in=[self.request.user.profile.team]).all()
        return queryset
    
    def get_context_data(self,**kwargs) :
        context = super(EventsRegisterListView,self).get_context_data(**kwargs)
        context["upcoming"] =Event.objects.filter(registration_starts__gte = timezone.now().date()).exclude(teams__in=[self.request.user.profile.team]).all()
        return context

"""