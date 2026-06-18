from django.urls import path
from . import views

app_name = "accounts"


urlpatterns = [

    path(
        "run/",
        views.run_workflow,
        name="run_workflow"
    ),

    path(
        "trends/",
        views.trending_topics,
        name="trending_topics"
    ),

    path(
        "generate-caption/",
        views.generate_caption,
        name="generate_caption"
    ),

    path(
        "generate-image/",
        views.generate_image,
        name="generate_image"
    ),

    path(
        "history/",
        views.content_history,
        name="content_history"
    ),
]
