# portal/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'post_type', 'meetup_time', 'meetup_location']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'meetup_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'meetup_location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide meetup fields by default, we'll show them with JavaScript
        self.fields['meetup_time'].required = False
        self.fields['meetup_location'].required = False