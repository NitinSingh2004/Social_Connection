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
    
    path('instagram_login/', views.instagram_login,
         name='instagram_login'),

    path('instagram_callback/', views.instagram_callback,
         name='instagram_callback'),

    path('linkedin_login/', views.linkedin_login,
         name='linkedin_login'),

    path('linkedin_callback/', views.linkedin_callback,
         name='linkedin_callback'),
    
    path('create_post/', views.create_post,
         name='create_post'),
    

]