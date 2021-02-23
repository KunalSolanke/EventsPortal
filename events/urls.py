from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import *

app_name="events"
urlpatterns = [
    path('register/',view=EventsRegisterListView.as_view(),name="event_list"),
    path('register/<int:pk>',view=EventRegisterView.as_view(),name='register_view'),
    path('register/<int:pk>/subteam',view=AddSubTeamView.as_view(),name='add_subteam'),
    path('submission/',view=EventsSubmissionListView.as_view(),name='submission_list'),
    path('submission/<int:pk>',view=EventSubmisionView.as_view(),name='event_submisision_detail'),
    path('submission/subteam/<int:pk>/',view=AddSubmission.as_view(),name='event_subteam_submisision'),
]