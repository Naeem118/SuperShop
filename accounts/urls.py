from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('adminsignup/', views.adminsignup, name='adminsignup'),
    path('adminsignin/', views.adminsignin, name='adminsignin'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('deleteprofile/', views.deleteprofile, name='deleteprofile'),
    path('addproduct/', views.addproduct, name='addproduct'),
] 