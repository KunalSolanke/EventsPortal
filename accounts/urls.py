from django.urls import path,include
from .views import *
app_name="accounts"
urlpatterns = [ 
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('login/',view=Home.as_view(),name="login_vew")
]