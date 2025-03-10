from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.models import Profile

# we need to add more datas in to our user creation form , so we created 
# a new form that inherits from Djangos 'UserCreationForm'.

class UserRegisterForm(UserCreationForm):
    email= forms.EmailField()

    class Meta: 
        model = User
        fields = ['username','email','password1','password2'] # Specify the field order 




class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField()

    class Meta: 
        model = User
        fields = ['username','email']




class ProfileUpdateForm(forms.ModelForm):
     class Meta:
          model = Profile
          fields = ['image']

