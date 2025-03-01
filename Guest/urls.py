from django.urls import path,include 
from Guest import views
app_name='Guest'

urlpatterns = [
    path('', views.Index, name='index'),
    path('signUp/', views.userEmail, name='signUp'),
    path('userRegistration/',views.userRegistration,name='userRegistration'),

    path('ajaxPlace/',views.ajaxPlace,name='ajaxPlace'),
    path('login/',views.login,name='login'),
]
