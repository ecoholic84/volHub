from django.urls import path,include 
from Admin import views
app_name='Admin'
urlpatterns = [
    path('district/',views.district,name='district'),
    path('deletedistrict/<int:did>',views.deletedistrict,name='deletedistrict'),
    path('editdistrict/<int:eid>',views.editdistrict,name='editdistrict'),

    path('adminRegistration/',views.adminRegistration,name='adminRegistration'),
    path('deleteAdmin/<int:did>',views.deleteAdmin,name='deleteAdmin'),
    path('editAdmin/<int:eid>',views.editAdmin,name='editAdmin'),
    path('adminDashboard/',views.adminDashboard,name='adminDashboard'),

    path('place/',views.Place,name="Place"),
    path('deletePlace/<int:did>',views.deletePlace,name="deletePlace"),
    path('editPlace/<int:eid>',views.editPlace,name='editPlace'),

    path('category/',views.category,name='category'),
    path('deleteCategory/<int:did>',views.deleteCategory,name='deleteCategory'),
    path('editCategory/<int:eid>',views.editCategory,name='editCategory'),

    path('subcategory/',views.Subcategory,name="subcategory"),
    path('editSubcategory/<int:eid>',views.editSubcategory,name="editSubcategory"),
    path('deleteSubcategory/<int:did>',views.deleteSubcategory,name="deleteSubcategory"),

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
]
