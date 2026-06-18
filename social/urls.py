from django.urls import path
from . import views

urlpatterns = [

    path(
        "connections",
        views.connections,
        name="connections"
    ),



    path('facebook_webhook/',
         views.facebook_webhook, name='facebook_webhook'),


    path('facebook_callback/', views.facebook_callback,
         name='facebook_callback'),

    path("publish_facebook/", views.publish_facebook,
         name="publish_facebook",),
    
    path('instagram_webhook/', views.instagram_webhook,
         name='instagram_webhook'),
    path('linkedin_webhook/', views.linkedin_webhook,
         name='linkedin_webhook'),
    
    path('create_post/', views.create_post,
         name='create_post'),
    

]