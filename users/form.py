from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '@username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'bio', 'profile_picture', 'is_artist')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email or Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'profile_picture', 'is_artist')