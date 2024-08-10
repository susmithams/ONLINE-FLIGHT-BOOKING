from django import forms
from django.contrib.auth.models import User
from .models import *
class SellerRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    cpassword=forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    email=forms.EmailField(required=True)
    phone=forms.IntegerField(label='phone',widget=forms.TextInput(attrs={'placeholder':'Enter your phone number'}))
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','phone','password','cpassword']


class NewPassengerForm(forms.ModelForm):
    fname=forms.CharField(label='First Name:',widget=forms.TextInput(attrs={'placeholder':'Enter your First Name'}))
    lname=forms.CharField(label='Last Name:',widget=forms.TextInput(attrs={'placeholder':'Enter your Last Name'}))
    age=forms.IntegerField(label='Age:',widget=forms.TextInput(attrs={'placeholder':'Enter your Age'}))
    gender=forms.CharField(label='Gender:',widget=forms.TextInput(attrs={'placeholder':'Enter your Gender'}))
    class Meta:
        model =NewPassenger
        fields = ['fname', 'lname', 'age', 'gender']

#
# class FlightFilterForm(forms.Form):
#     ECONOMY = '0'
#     BUSINESS = '1'
#     FIRST_CLASS = '2'
#     CATEGORY_CHOICES = [
#         (ECONOMY, 'economy'),
#         (BUSINESS, 'business'),
#         (FIRST_CLASS, 'firstclass')
#     ]
#     category = forms.MultipleChoiceField(
#         choices=CATEGORY_CHOICES,
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )