from django.urls import path,include
from django.contrib.auth.views import LogoutView
from .views import *

app_name="accounts"

urlpatterns = [ 
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('signup/complete/',view=UserSignupCompleteView.as_view(),name='register_view'),
    path('team/create/',view=TeamCreateView.as_view(),name='create_team'),
    path('profile/',view=ProfileView.as_view(),name='profile'),
    path("",include("django.contrib.auth.urls"))
]