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

    path('industries/', views.Industry, name='industries'),
    path('editIndustry/<int:eid>', views.editIndustry, name='editIndustry'),
    path('deleteIndustry/<int:did>', views.deleteIndustry, name='deleteIndustry'),

    path('skills/', views.industry_list, name='skills'),
    path("add-industry/", views.add_industry, name="add_industry"),
    path("add-skill/", views.add_skill, name="add_skill"),
    path("edit-skill/", views.edit_skill, name="edit_skill"),
    path("delete-skill/", views.delete_skill, name="delete_skill"),

]
