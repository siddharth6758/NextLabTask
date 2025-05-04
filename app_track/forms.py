from django import forms
from app_track.models import Apps, UserAppInstall

class AppsForm(forms.ModelForm):
    class Meta:
        model = Apps
        fields = ['app_logo', 'name', 'category', 'sub_category', 'points']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-section'}),
            'category': forms.Select(attrs={'class': 'form-section'}),
            'sub_category': forms.Select(attrs={'class': 'form-section'}),
            'points': forms.NumberInput(attrs={'class': 'form-section'}),
            'app_logo': forms.ClearableFileInput(attrs={'class': 'form-section', 'style': 'padding: 5px;'})
        }

class AppsInstallForm(forms.ModelForm):
    class Meta:
        model = UserAppInstall
        fields = ['screenshot']
        widgets = {
            'screenshot': forms.ClearableFileInput(attrs={'class': 'form-section', 'style': 'padding: 5px;'})
        }