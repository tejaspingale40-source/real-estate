from django import forms
from .models import Property, PropertyImage, PropertyVideo, Amenity


class PropertyForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'amenity-checkbox'}),
        required=False
    )

    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'location', 'address',
            'property_type', 'purpose', 'bedrooms', 'bathrooms', 'area',
            'parking', 'furnished', 'status', 'featured', 'amenities'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Luxury 3 BHK Villa'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide complete property description...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in INR'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Solapur'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Full street address'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'purpose': forms.Select(attrs={'class': 'form-select'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area in sq.ft'}),
            'parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'furnished': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_cover', 'order']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_cover': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class PropertyVideoForm(forms.ModelForm):
    class Meta:
        model = PropertyVideo
        fields = ['video', 'title']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Video Title (Optional)'}),
        }


from .models import SiteSettings

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'tagline', 'phone', 'email', 'address',
            'about_subtitle', 'about_vision_heading', 'about_vision_text', 'about_quote', 'about_founder_name',
            'contact_subtitle', 'contact_address', 'contact_hours', 'google_maps_url'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-input'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'about_subtitle': forms.TextInput(attrs={'class': 'form-input'}),
            'about_vision_heading': forms.TextInput(attrs={'class': 'form-input'}),
            'about_vision_text': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'about_quote': forms.TextInput(attrs={'class': 'form-input'}),
            'about_founder_name': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_subtitle': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'contact_hours': forms.TextInput(attrs={'class': 'form-input'}),
            'google_maps_url': forms.URLInput(attrs={'class': 'form-input'}),
        }
