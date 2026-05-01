from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12;'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '@username',
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12;'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12;'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12;'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Email or Username',
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12;'
        })
    )

class UserProfileForm(forms.ModelForm):
    display_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Your display name (optional)', 
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12;'
        }), 
        required=False
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about your artistic journey...', 
            'rows': 4,
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12; resize: vertical;'
        }), 
        required=False
    )
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={
            'style': 'width: 100%; padding: 0.75rem; border: 1px solid #d6c9b0; border-radius: 6px; font-family: Jost, sans-serif; font-size: 0.9rem; background: #fdfaf5; color: #2b1d12;'
        }),
        required=False
    )
    is_artist = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'style': 'width: auto; margin-right: 0.5rem;'
        }),
        required=False
    )
    
    class Meta:
        model = User
        fields = ('display_name', 'bio', 'profile_picture', 'is_artist')