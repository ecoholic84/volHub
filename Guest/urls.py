from django.urls import path,include 
from Guest import views
app_name='Guest'

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.get_email, name='sign_up'),
    path('user-registration/', views.user_registration, name='user_registration'),
    path('user_who/', views.user_who, name='user_who'),
    path('login/', views.login, name='login'),
    path('ajax_place/', views.ajax_place, name='ajax_place'),
    path('profile/<str:name>',views.profile, name="profile"),

    path('forgotpassword/',views.forgotpassword,name="forgotpassword"),
    path('otp/',views.otp,name="otp"),
    path('newpass/',views.newpass,name="newpass"),
    path('public-event/<int:event_id>/', views.public_event_detail, name="public_event_detail"),
]
