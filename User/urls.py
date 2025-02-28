from django.urls import path,include 
from User import views
app_name='User'
urlpatterns = [
    path('userDashboard/', views.userDashboard, name='userDashboard'),

    path('myProfile/', views.myProfile, name='myProfile'),
    path('editProfile/', views.editProfile, name='editProfile'),

    path('changePassword/', views.changePassword, name='changePassword'),

    path('feedback/', views.Feedback, name='feedback'),
    path('deleteFeedback/<int:did>', views.deleteFeedback, name='deleteFeedback'),
    
    path('complaint/', views.Complaint, name='complaint'),
    path('deleteComplaint/<int:did>', views.deleteComplaint, name='deleteComplaint'),
    path('editComplaint/<int:eid>', views.editComplaint, name='editComplaint'),
]
