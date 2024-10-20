from django import forms
from user_moudle.models import custom_user

class Login_Form(forms.Form):
    username=forms.CharField(max_length=60,label='username',required=False,
                             error_messages={'required':'you cant leave this field empty'},widget=forms.TextInput(attrs=
                             {'placeholder':'Your Username','class':'login_input'}))
    password=forms.CharField(required=False,
        widget=forms.PasswordInput(attrs={'class':'login_input','placeholder':'Your Password'}),label='password')

class SignUp_Form(forms.ModelForm):
    class Meta:
        model=custom_user
        fields=['email','first_name','last_name','username','birth_date','password']
        labels={'first_name':'firstname','last_name':'lastname','username':'username','password':'password','birth_date':'birth_date'}
        widgets={'password':forms.PasswordInput(),'birth_date':forms.SelectDateWidget()}
