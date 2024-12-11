from . import views
from django.urls import path, include
from django.contrib.auth.views import PasswordChangeView



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

  

    #Legal
    path('terms-and-condition/', views.terms_and_condition, name='terms_and_condition'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),

]
