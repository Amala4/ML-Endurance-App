from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from .models import (
    UserProfile,
)
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














#Other forms
# class InquiryForm(forms.ModelForm):
#     class Meta:
#         model = Inquiry
#         fields = ['question']


#     def save(self, commit=True, patient=None):
#         inquiry = super().save(commit=False)


#         # Set the patient
#         inquiry.patient = patient
#         inquiry.store_branch_model = patient.home_branch
#         inquiry.date_created = date.today().strftime('%d/%m/%Y')

#         if commit:
#             inquiry.save()

#         return inquiry







# class InterestForm(forms.ModelForm):
#     class Meta:
#         model = Registration
#         fields = ['first_name', 'surname', 'email', 'confirm_email', 'phone_no', 'address1', 'address2', 'state', 'suburb', 'post_code', 'current_at_options', 'home_branch']

#     confirm_email = forms.EmailField(
#         label='Confirm Email',
#         required=True,
#         help_text='Please enter your email address again for confirmation.',
#     )


#     current_at_options = forms.TypedChoiceField(
#         label='Is your current contact lens prescription at Options?',
#         required=True,
#         choices=((True, 'Yes'), (False, 'No')),
#         widget=forms.RadioSelect,
#         coerce=lambda x: x == 'True',
#         initial=False
#     )

#     def __init__(self, *args, **kwargs):
#         super(InterestForm, self).__init__(*args, **kwargs)
#         # Set all fields except 'address2' as compulsory
#         for field_name, field in self.fields.items():
#             if field_name != 'address2':
#                 field.required = True


#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         confirm_email = cleaned_data.get('confirm_email')

#         if email and confirm_email and email != confirm_email:
#             raise forms.ValidationError("Email addresses do not match.")

#         return cleaned_data


#     def save(self, commit=True, patient=None):
#         interest = super().save(commit=False)


#         # Set the date
#         interest.date_submitted = date.today().strftime('%d/%m/%Y')

#         if commit:
#             interest.save()

#         return interest






# attrs={'class': 'form-control'}
# class CartReorderAddForm(forms.Form):
#     options = forms.ChoiceField(required=False, widget=forms.Select(attrs={'id': 'reorder_option', 'class': 'form-control'}))


#     def __init__(self, *args, **kwargs):
#         super(CartReorderAddForm, self).__init__(*args, **kwargs)
#         self.fields['options'].label = ''
#         frequencies = Reorder_Discount.objects.all()
#         FREQUENCY_CHOICES = [
#                 ('-1', '<please select> '),
#                 ('0', 'No thanks'),
#             ]
#         for item in frequencies:
#             new_choice = (item.frequency, str(item))
#             FREQUENCY_CHOICES.append(new_choice)

#         # Set the choices for the 'options' field
#         self.fields['options'].choices = FREQUENCY_CHOICES
#         self.fields['options'].initial = '-1'



