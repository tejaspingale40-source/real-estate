from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone', 'email', 'message', 'property']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about your requirements...', 'required': True}),
            'property': forms.HiddenInput(),
        }


class EnquiryStatusForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select-sm'}),
        }
