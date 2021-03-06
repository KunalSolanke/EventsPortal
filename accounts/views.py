from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import UpdateView,CreateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Team,Profile,generateAlcherId
from .mixins import ProfileMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import EmailValidator,RegexValidator
from django.contrib.auth import update_session_auth_hash
from events.views import get_registered_events
from django.db import transaction
import json
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
# Create your views here.


# class UserSignupCompleteView(LoginRequiredMixin,UpdateView) :
class UserSignupCompleteView(UpdateView) :
   model = User
   template_name = "accounts/signup_complete.html"
   
   def get(self,request):
         return render(request,self.template_name)
   
   @transaction.atomic
   def post(self,request,*args,**kwargs) :
        password = request.POST.get("password",None)
        username = request.POST.get("username",None)
        cnf_password = request.POST.get("confirm_password",None)
        firstName = request.POST.get("first_name",None)
        lastName = request.POST.get("last_name",None)
        phone = request.POST.get("phone",None)
        college = request.POST.get("college",None)
        email = request.POST.get("email", None)

        name_validator = RegexValidator("^(?!\s*$).+")
        phone_validator = RegexValidator('^[0-9]{10}$')
        errors ={}


        try :
            name_validator(firstName)
        except Exception as e :
            errors["fullName_error"]="First Name should not be empty"
        
        try :
            name_validator(username)
        except Exception as e :
            errors["invalid_username_error"]="Name should not be empty"
        
        if User.objects.filter(username=username).exists() :
             errors["username_error"]="Person with same username exists"
        
        try :
            name_validator(college)
        except Exception as e :
            errors["college_error"]="college name  should not be empty"

        try :
            phone_validator(phone)
        except Exception as e :
            errors["phone_error"]="Must have 10 digits and only digits from 0 to 9  should not"
        
        print(errors)
        if errors : 
            errors["stat"]=400
            return JsonResponse(errors)

        if password != cnf_password :
            errors["stat"]=400
            errors["password_error"]="Passwords don't match"
            return JsonResponse(errors)
        

        print("########################################################")
        user = User.objects.create_user(username=username, email=email, password=password)
        print(user.username)
        print(user.email)
        print(user.password)

        alcher_id = generateAlcherId(firstName)
        user.alcher_id = alcher_id
        user.first_name = firstName
        user.last_name = lastName
        user.save()
        user = authenticate(request, username=username, password=password)    

        print("Here")
        print(user)
        try : 
           user.set_password(password)
        except : 
            errors["stat"]=400
            errors["password_error"]="Password should not be similar to username or fullname"
            return JsonResponse(errors)
            
        
        # user = request.user
        # user = authenticate(request, username)
        print(user)
        fullName = firstName + " " + lastName
        user.profile.fullname = fullName
        alcher_id = generateAlcherId(firstName)
        user.profile.alcher_id = alcher_id
        user.profile.phone = phone
        user.profile.college = college
        update_session_auth_hash(request,user)
        user.profile.is_signup_complete = True
        user.profile.is_profile_complete = False
        user.profile.save()
        
        print(user,user.profile)
        errors["stat"]=200
        errors.update({"fullname":fullName,"alcher_id":user.profile.alcher_id})
        return JsonResponse(errors)


class TeamCreateView(LoginRequiredMixin,CreateView) :
    model = Team
    template_name ="accounts/team_info.html"

    def get(self,request):
         return render(request,self.template_name)

    @transaction.atomic
    def post(self,request,*args,**kwargs) :
        body = json.loads(request.body)
        name = body.get("team_name",None)
        members = body.get("members",None)
        name_validator = RegexValidator("^(?!\s*$).+")
        errors ={}
        print(body)
        
        try :
            name_validator(name)
        except Exception as e :
            errors["team_name_error"]="Name should not be empty"
        
        if Team.objects.filter(team_name=name).exists() :
            errors["team_name_error"]="Team with same name exists."
        
        print(errors)
        if errors :
                errors["stat"]=400
                return JsonResponse(errors)
        
    
        
        user=request.user
        team = Team.objects.create(team_name=name,leader=request.user)
        
        for member in members : 
            name = member.get('name')
            phone = member.get("phone")
            email = member.get("email")

            users = User.objects.filter(email=email)
            if users.exists() :
                team.members.add(users[0].profile)
                continue
            
            member= User.objects.create(username=name,email=email)
            member.profile.phone = phone
            alcher_id  = generateAlcherId(name)
            member.profile.alcher_id = alcher_id
            member.profile.fullname=name
            member.profile.save()
            team.members.add(member.profile)

        user.profile.is_profile_complete= True

        user.profile.team = team
        user.profile.save()
        
        errors["stat"]=200
        return JsonResponse(errors)


class ProfileView(ProfileMixin,View):
    template_name = "accounts/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["team"] = self.request.user.profile.team
        context["team_members"] =self.request.user.profile.team.members.all()
        context["registered_events"]=get_registered_events(self.request.user)
        return context
    
    def get(self,request):
        context={}
        context["team"] = self.request.user.team
        context["team_members"] =self.request.user.team.members.all()
        context["registered_events"]=get_registered_events(self.request.user)
        return render(request,self.template_name,context)



# class AddMember(LoginRequiredMixin,View) :
#     template_name = "accounts/member.html"
    
#     def get(self,request,*arg,**kwargs):
#         return render(request,self.template_name)

#     def post(self,request,*args,**kwargs) :
#         alcher_id = request.POST.get("alcher_id",None)
#         if alcher_id :

#             if not Profile.objects.filter(alcher_id=alcher_id).exists() :
#                 errors["alcher_id_error"]="No alcher id found"

#             if errors :
#                 return render(request,self.template_name,errors)
            
#             profile = get_object_or_404(Profile,alcher_id)
#             request.user.team.add(Profile,alcher_id=alcher_id)
#             request.user.team.save()
#         else :
#             name = request.POST.get("username",None)
#             email = request.POST.get("email",None)
#             phone = request.POST.get("phone",None)
#             gender = request.POST.get("gender",None)
            
#             name_validator = RegexValidator("^(?!\s*$).+")
#             phone_validator = RegexValidator('^[0-9]{10}$')
#             errors ={}

#             try :
#                 name_validator(fullName)
#             except Exception as e :
#                 errors["fullName_error"]="Name should not be empty"
            
#             try :
#                 EmailValidator(email)
#             except Exception as e :
#                 errors["email_error"]="Must have 10 digits and only digits from 0 to 9  should not"
            
#             try :
#                 phone_validator(phone)
#             except Exception as e :
#                 errors["phone_error"]="Must have 10 digits and only digits from 0 to 9  should not"
            
            
#             if errors :
#                 errors["stat"]=400
#                 return JsonResponse(errors)


#             user = User.objects.create(username=name,email=email)
#             user.profile.phone = phone
#             user.profile.is_profile_complete = True
#             user.profile.gender = gender
#             user.profile.team = request.user.team
#             user.profile.save()
        
#         errors["stat"]=200
#         return JsonResponse(errors)