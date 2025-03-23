from django.urls import path,include 
from Guest import views
app_name='Guest'

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.get_email, name='sign_up'),
    path('user-registration/', views.user_registration, name='user_registration'),
    path('user-type/', views.user_who, name='user_who'),


    path('ajax-place/',views.ajax_place,name='ajax_place'),
    path('login/',views.login,name='login'),

]
