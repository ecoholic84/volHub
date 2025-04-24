from django.urls import path,include 
from Admin import views
app_name='Admin'
urlpatterns = [

    path('adminDashboard/',views.adminDashboard,name='adminDashboard'),
    
    path('feedbacks/', views.feedback_list, name='feedback_list'),
    path('logout/', views.logout, name='logout'),

    path('adminRegistration/',views.adminRegistration,name='adminRegistration'),
    path('deleteAdmin/<int:did>',views.deleteAdmin,name='deleteAdmin'),
    path('editAdmin/<int:eid>',views.editAdmin,name='editAdmin'),


    path('type/',views.types,name="type"),
    path('deleteType/<int:did>',views.deleteType,name="deleteType"),
    path('editType/<int:eid>',views.editType,name="editType"),

    path('complaintInbox/',views.complaintInbox,name="complaintInbox"),
    path('replyCompliant/<int:rid>',views.replyCompliant, name='replyCompliant'),

    path('industry-skills/', views.industrySkills, name='industrySkills'),
    path('add-industry/', views.addIndustry, name='addIndustry'),
    path('add-skill/', views.addSkill, name='addSkill'),
    path('edit-skill/<int:sid>/', views.editSkill, name='editSkill'),
    path('delete-skill/<int:sid>/', views.deleteSkill, name='deleteSkill'),
    path('delete-industry/<int:iid>/', views.deleteIndustry, name='deleteIndustry'),

    path('country-state-city/', views.country_state_city, name='country_state_city'),
    path('add-country/', views.add_country, name='add_country'),
    path('add-state/', views.add_state, name='add_state'),
    path('add-city/', views.add_city, name='add_city'),
]
