from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth import login

class ProfileMixin(LoginRequiredMixin) :

    def dispatch(self,request,*args,**kwargs) :
        user = request.user
        print(user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        if user.profile.is_profile_complete and user.profile.is_signup_complete :
            return super().dispatch(request,*args,**kwargs)
        elif not user.profile.is_signup_complete :
            return redirect("/accounts/signup/complete")
        elif not  user.profile.is_profile_complete:
            return redirect("/accounts/team/create")
        return super().dispatch(request,*args,**kwargs)