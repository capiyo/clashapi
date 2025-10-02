from django.urls import path
from .views import register, loginUser, getMyDetails, logout, postMessage,getAllGames,pledging,get_pledges,add_post,get_posts

urlpatterns = [
    
    path('clash/register',register,name="register"),
    path('clash/getAllGames',getAllGames,name="getAllGames"),
    path('clash/pledging',pledging,name="pledging"),
    path('clash/getPledges',get_pledges,name="get_pledges"),
    path('clash/add_post',add_post,name="add_post"),
    path('clash/get_posts',get_posts,name="get_posts"),
    
    path('gighub/postMessage',postMessage,name="postMessage"),
   
    path('clash/login', loginUser, name="login"),
    path('gighub/getMyDetails', getMyDetails, name="getMyDetails"),
     path('gighub/logout', logout, name="get_details"),
    
   
    
]
