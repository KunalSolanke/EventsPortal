from django.urls import path,include
from .views import *
app_name="accounts"
urlpatterns = [ 
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('login/',view=Login.as_view(),name="login_vew"),
    path('register/',view=UserSignupCompleteView.as_view(),name='register_view'),
    path('team/create',view=TeamCreateView.as_view(),name='create_team'),
    path('profile/',view=ProfileView.as_view(),name='profile'),
    path('profile/addMember/',view=AddMember.as_view(),name='add_member'),
]