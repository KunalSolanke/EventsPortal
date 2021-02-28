from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import UpdateView,CreateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Team,Profile
from .models import generateAlcherId
from .mixins import ProfileMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import EmailValidator,RegexValidator
# Create your views here.

class Login(View) :
    template_name = "accounts/login.html"
    def get(self,request):
         return render(request,self.template_name)


class UserSignupCompleteView(LoginRequiredMixin,UpdateView) :
   model = User
   template_name = "accounts/signup_complete.html"
   
   def get(self,request):
         return render(request,self.template_name)

   def post(self,request,*args,**kwargs) :
        password = request.POST.get("password",None)
        cnf_password = request.POST.get("confirm_password",None)
        fullName = request.POST.get("full_name",None)
        phone = request.POST.get("phone",None)
        gender = request.POST.get("gender",None)
        college = request.POST.get("college",None)
        
        name_validator = RegexValidator("^(?!\s*$).+")
        phone_validator = RegexValidator('^[0-9]{10}$')
        try :
            name_validator(fullName)
        except Exception as e :
            errors["fullName_error"]="Name should not be empty"
        
        try :
            name_validator(college)
        except Exception as e :
            errors["college_error"]="college name  should not be empty"
        
        try :
            phone_validator(phone)
        except Exception as e :
            errors["phone_error"]="Must have 10 digits and only digits from 0 to 9  should not"
        
        user = request.user 
        user.profile.fullname = fullName
        user.phone = phone
        user.profile.gender = gender if gender is not None else "M"
        user.set_password(password)
        user.profile.is_signup_complete = True
        user.profile.is_profile_complete = False
        user.save()
        user.profile.save()
        print(user,user.profile)
        return redirect("/accounts/profile")

class TeamCreateView(LoginRequiredMixin,CreateView) :
    model = Team
    template_name ="accounts/team_info.html"

    def get(self,request):
         return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs) :
        name = request.POST.get("team_name",None)
        college = request.POST.get("college",None)
        city = request.POST.get("city",None)
        info = request.POST.get("info",None)
        user=request.user
        team = Team.objects.create(team_name=name,city=city,leader=request.user,description=info)
        user.profile.is_profile_complete= True
        user.profile.team = team
        user.profile.save()
        return redirect("/accounts/profile/add_member")



class ProfileView(ProfileMixin,View):
    template_name = "accounts/profile.html"
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["team"] = self.request.user.profile.team
        context["team_members"] =self.request.user.profile.team.members.all()
        return context
    
    def get(self,request):
         return render(request,self.template_name)

class AddMember(LoginRequiredMixin,View) :
    template_name = "accounts/member.html"
    
    def get(self,request,*arg,**kwargs):
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
            user.profile.team = request.user.team
            user.profile.save()
        return redirect("/accounts/profile/add_member")