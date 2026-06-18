from django.urls import path
from . import views

urlpatterns = [

    path(
        "scheduler/",
        views.scheduler,
        name="scheduler",
    ),
    
    path(
        "calendar/",
        views.calendar,
        name="calendar",
    ),
]
