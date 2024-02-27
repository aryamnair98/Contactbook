from django.urls import path, include
from.import views

urlpatterns = [
    path("login/", views.loginView, name="loginView"),
     path("", views.registration, name="registration"),
    path('index',views.index,name="index"),
    path('add-contact/',views.addContact,name="add-contact"),
    path('edit-contact/<str:pk>', views.editContact, name='edit-contact'),
    path('delete/<str:pk>', views.deleteContact, name='delete'),
    path('profile/<str:pk>', views.contactProfile, name='profile'),
    path('add-favorites/', views.add_favorites, name='add-favorites'),
    path('add-to-favorites/<int:contact_id>/', views.add_to_favorites, name='add-to-favorites'),
    path('remove-from-favorites/<int:contact_id>/', views.remove_from_favorites, name='remove-from-favorites'),
    path('view-favourites/', views.view_favourites, name='view-favourites'),
    path('view-group/<int:group_id>/', views.view_group, name='view_group'),
    path('view_groups/', views.view_groups, name='view_groups'),
    path('create-group/', views.create_group, name='create-group'),
    path('add-members-to-group/<int:group_id>/', views.add_members_to_group, name='add-members-to-group'),
    path('save-group/<int:group_id>/', views.save_group, name='save-group'),
    path('logout/', views.logout, name='logout'),
    
]