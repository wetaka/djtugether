from django.urls import path
from tugether import views

urlpatterns = [
    path('user', views.user_list),
    path('user/<int:pk>', views.user_detail),
    # path('login', views.login),
    path('chk-first-login/<str:userid>',views.check_login),

    path('event', views.event_list),
    path('event/<int:pk>', views.event_detail),

    path('comment', views.comment_list),
    path('comment/<int:pk>', views.comment_detail),

    path('category', views.category_list),
    path('category/<int:pk>', views.category_detail),
]