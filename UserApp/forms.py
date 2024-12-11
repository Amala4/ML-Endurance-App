from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

#Admin forms
class AdminUserCreationForm(UserCreationForm):

    class Meta():
        model = CustomUser
        fields = ('email', 'password1', 'password2')



class AdminUserChangeForm(UserChangeForm):

    class Meta():
        model = CustomUser
        fields = ('email', 'password',)





