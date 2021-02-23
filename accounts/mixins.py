from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class ProfileMixin(LoginRequiredMixin) :

    def dispatch(self,request,*args,**kwargs) :
        user = request.user
        print(user)
        if user.profile.is_profile_complete and user.profile.is_signup_complete :
            return super().dispatch(request,*args,**kwargs)
        elif not user.profile.is_signup_complete :
            return redirect("/accounts/signup/complete")
        elif not  user.profile.is_profile_complete:
            return redirect("/accounts/team/create")
        return super().dispatch(request,*args,**kwargs)