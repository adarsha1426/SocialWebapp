from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(label="Password", widget=forms.PasswordInput)

    username.widget.attrs.update({"class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"})
    password.widget.attrs.update({"class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"})

class RegisterForm(forms.ModelForm):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirm Password" , widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']
        widgets={
        'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your last name',
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your email',
            }),
          

    }
        #explicitly defining password fields to override the custom the password field
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your password',
        })
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirm your password',
        })
    )
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password1']!=cd['password2']:
            raise forms.ValidationError("The two password did not match.")
        return cd['password2']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_pic','date_of_birth','bio',]

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username']