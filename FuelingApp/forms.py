from django import forms
from .models import Support

class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['message', 'attachment'] 
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'textarea-field',
                'rows': 5,
                'cols': 40,
                'placeholder': 'Share your suggestions, support requests and other feedback',
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'file1',
                'style': 'visibility: hidden; height: 0; width: 0',
                'accept': 'image/*',
            }),
        }
