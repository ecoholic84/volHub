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

    path('profile/', views.profile, name='profile'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('create-vol-profile/', views.create_vol_profile, name='create_vol_profile'),
    path('create-organizer-profile/', views.create_organizer_profile, name='create_organizer_profile'),
    path('profile-country-ajax/', views.profile_country_ajax, name='profile_country_ajax'),
    path('profile-state-ajax/', views.profile_state_ajax, name='profile_state_ajax'),

    path('event/',views.Event,name="Event"),

    # Dashboard redirection views
    path('volunteer-dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('organizer-dashboard/', views.organizer_dashboard, name='organizer_dashboard'),

    # Volunteer request action
    path('event-detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('profile/edit/<int:page>/', views.edit_profile, name='edit_profile'),
    path('ajax/skill-search/', views.skill_search_ajax, name='skill_search_ajax'),

    # Organizer actions
    path('event-action/<int:event_id>/', views.event_action, name='event_action'),

]
