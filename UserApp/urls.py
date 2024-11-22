from . import views
from django.urls import path, include
from django.contrib.auth.views import PasswordChangeDoneView,PasswordChangeView



urlpatterns = [
    #Default django urls
    path('password_change/',
         PasswordChangeView.as_view(template_name="registration/change_password.html"),
         name='password_change'),

    path('', include('django.contrib.auth.urls')),

    #User url
    path('user_login/', views.user_login, name ='user_login'),
    path('signup/', views.sign_up, name ='signup'),
    path('profile/', views.profile, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),

  

    #Contact Us
    # path('make-inquiry/', views.Make_Inquiry, name='make_inquiry'),

]
