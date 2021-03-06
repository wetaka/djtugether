from django.urls import path
from tugether import views

urlpatterns = [
    path('user', views.user_list),
    path('user/<int:pk>', views.user_detail),
    # path('login', views.login),
    path('chk-first-login/<str:userid>',views.check_login),

    path('event', views.event_list),
    path('event/<int:pk>', views.event_detail),
    path('get-your-event-approve/<str:userid>',views.get_yourevent),
    path('get-your-event-waitapprove/<str:userid>',views.get_youreventwait),
    
    path('get-join/<int:eventid>',views.get_join),
    path('search-event/<int:categoryid>',views.get_searchevent),
    path('upcoming-event/<str:userid>',views.get_upcomingevent),
    path('past-event/<str:userid>',views.get_pastevent),
    path('get-autowords/<str:word>/<int:categoryid>',views.get_autoCompleteWords),

    path('noti', views.noti_list),
    path('noti/<int:pk>', views.noti_detail),
    
    path('comment', views.comment_list),
    path('comment/<int:pk>', views.comment_detail),
    path('comment-event/<int:eventid>',views.get_comment),

    path('category', views.category_list),
    path('category/<int:pk>', views.category_detail),
    path('redirect/tu/', views.redirectURL), 
]