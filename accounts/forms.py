# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import AlumniUser

# This helper adds the 'form-control' class to all fields
class BootstrapFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add the Bootstrap class to all fields
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
            
            # Add placeholders
            if field_name == 'email':
                field.widget.attrs['placeholder'] = 'name.surname@mitwpu.edu'
            if field_name == 'full_name':
                field.widget.attrs['placeholder'] = 'Jane Doe'
            if field_name == 'phone_number':
                field.widget.attrs['placeholder'] = '+91 9XXXXXXXXX'
            if field_name == 'batch_year':
                field.widget.attrs['placeholder'] = '2025'

# Update your forms to use the Mixin
class AlumniUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = AlumniUser
        # --- !! ADDED 'user_type' TO THIS LIST !! ---
        fields = ('full_name', 'email', 'user_type', 'phone_number', 'batch_year')

class AlumniUserChangeForm(BootstrapFormMixin, UserChangeForm):
    class Meta:
        model = AlumniUser
        fields = ('full_name', 'email', 'phone_number', 'batch_year')

# Update the Login Form
class AlumniAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'name.surname@mitwpu.edu'
        self.fields['password'].widget.attrs['placeholder'] = '••••••••'


# --- !! THIS IS THE NEW FORM FOR EDITING YOUR PROFILE !! ---
class ProfileEditForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AlumniUser
        fields = ('full_name', 'phone_number', 'batch_year', 'is_mentor')
        widgets = {
            # This makes the mentor field a nice checkbox
            'is_mentor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hide the 'is_mentor' checkbox if the user is a Student
        if self.instance and self.instance.user_type == 'Student':
            self.fields['is_mentor'].widget = forms.HiddenInput()
            self.fields['is_mentor'].required = False