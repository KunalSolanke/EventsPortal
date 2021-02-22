from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import UpdateView,CreateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Team,Profile
from .models import generateAlcherId
# Create your views here.

class Login(View) :
    template_name = "accounts/login.html"
    def get(self,request):
         return render(request,self.template_name)


class UserSignupCompleteView(UpdateView) :
   model = User
   template_name = "accounts/signup_complete.html"
   
   def get(self,request):
         return render(request,self.template_name)

   def post(self,request,*args,**kwargs) :
        password = request.POST.get("password",None)
        cnf_password = request.POST.get("confirm_passowrd",None)
        fullName = request.POST.get("full_name",None)
        phone = request.POST.get("phone",None)
        gender = request.POST.get("gender",None)

        user = request.user 
        user.profile.fullname = fullName
        user.phone = phone
        user.profile.gender = gender
        user.set_password(password)
        user.profile.is_profile_signup_complete = True
        user.profile.save()
        return redirect("/profile")

class TeamCreateView(View) :
    model = Team
    template_name ="accounts/team_info.html"

    def get(self,request):
         return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs) :
        name = request.POST.get("name",None)
        college = request.POST.get("college",None)
        city = request.POST.get("city",None)
        info = request.POST.get("city",None)

        team = Team.objects.create(team_name=name,city=city,leader=request.user,info=info)
        user.profile.is_profile_complete= True
        user.profile.college = college
        user.profile.save()
        return redirect("/profile")



class ProfileView(View):
    template_name = "accounts/profile.html"
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["team"] = self.request.user.profile.team
        context["team_members"] =self.request.user.profile.team.members.all()
        return context
    
    def get(self,request):
         return render(request,self.template_name)

class AddMember(View) :
    template = "accounts/member.html"
    
    def get(self,requset,*arg,**kwargs):
        return render(request,self.template_name)

    def post(self,request,*args,**kwargs) :
        alcher_id = request.POST.get("alcher_id",None)
        if alcher_id :
            profile = get_object_or_404(Profile,alcher_id)
            request.user.team.add(Profile,alcher_id=alcher_id)
            request.user.team.save()
        else :
            name = request.POST.get("username",None)
            email = request.POST.get("email",None)
            phone = request.POST.get("phone",None)
            gender = request.POST.get("gender",None)
            
            user = User.objects.create(username=name,email=email)
            user.profile.phone = phone
            user.profile.is_profile_complete = True
            user.profile.gender = gender
            user.profile.save()
        return redirect("/team_info")


            
