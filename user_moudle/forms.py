from django import forms
from django.core.exceptions import ValidationError

from .models import User_Report
import re
class Report_Form(forms.ModelForm):
    class Meta:
        model =User_Report
        fields=['reason','made_by','parent_list']
        labels={'reason':'why are you reporting this user'}
        widgets={'made_by':forms.TextInput(attrs={'style':'display:none'}),'parent_list':forms.TextInput(attrs={'style':'display:none'})}

def passowrd_validator(value):
    escaped_chars = re.escape('!@#$%^&*()')
    pat = f'(?=.*[A-Z].*)(?=.*[a-z])(?=.*[0-9].*)(?=.*[{escaped_chars}].*)'
    if not re.match(pat,value):
        raise ValidationError('Password Not Srong enought')


class Password_Reset_Form(forms.Form):
    password=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'password','name':'password'}),validators=[passowrd_validator])
    password_repeat=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'password_repeat','name':'password_repeat'
                                                                                    }),validators=[passowrd_validator])