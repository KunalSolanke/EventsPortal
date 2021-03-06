from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import *

app_name="events"


urlpatterns = [
    path('register/<str:event_name>/',view=EventRegisterView.as_view(),name='register_view'),
    path('register/<str:event_name>/subteam/',view=AddSubTeamView.as_view(),name='add_subteam'),
    path('submission/subteam/<int:pk>/',view=AddSubmission.as_view(),name='event_subteam_submisision'),
]