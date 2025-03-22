from django.urls import path,include 
from User import views
app_name='User'
urlpatterns = [
    path('logout/', views.logout, name='logout'),

    path('myProfile/', views.myProfile, name='myProfile'),
    path('editProfile/', views.editProfile, name='editProfile'),

    path('changePassword/', views.changePassword, name='changePassword'),

    path('feedback/', views.Feedback, name='feedback'),
    path('deleteFeedback/<int:did>', views.deleteFeedback, name='deleteFeedback'),
    
    path('complaint/', views.Complaint, name='complaint'),
    path('deleteComplaint/<int:did>', views.deleteComplaint, name='deleteComplaint'),
    path('editComplaint/<int:eid>', views.editComplaint, name='editComplaint'),

    path('create-profile/', views.create_profile, name='create_profile'),
    path('profile-country-ajax/', views.profile_country_ajax, name='profile_country_ajax'),
    path('profile-state-ajax/', views.profile_state_ajax, name='profile_state_ajax'),

    path('event/',views.Event,name="Event"),

    # Dashboard redirection views
    path('volunteer-dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('organizer-dashboard/', views.organizer_dashboard, name='organizer_dashboard'),

    # Volunteer request action
    path('request-to-volunteer/<int:event_id>/', views.request_to_volunteer, name='request_to_volunteer'),

    path('event-detail/<int:event_id>/', views.event_detail, name='event_detail'),

]
