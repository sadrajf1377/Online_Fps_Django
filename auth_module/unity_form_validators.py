
from utils.Email_Sending import Send_Email_To
from user_moudle.models import custom_user
def validate_password(password, password_repeat):
    errors = []
    if password != password_repeat:
        errors.append("Passwords Don't Match")
    if len(password) < 8:
        errors.append("Password should contain at least 8 characters!")
    if not any([x for x in password if not x.isalnum()]):
        errors.append('Password must Contain At least One Special Character like &,$,%,@ etc!')
    if password.isupper():
        errors.append('Password should contain at least lower character')
    if password.islower():
        errors.append('Password should contain at least Upper character')
    if password.isnumeric():
        errors.append('Password should not be entirely numeric,it must have othe characters as well!')
    if password.isalpha():
        errors.append('Password should contain at least one number')
    return errors
class Unity_Form_Validate:
    def Validate_SignUp_Form(self,post_request,act_code):
        password=post_request.get('password')
        password_repeat=post_request.get('password_repeat')
        birth_day=int(post_request.get('birth_day'))
        birth_month=int(post_request.get('birth_month'))
        birth_year=int(post_request.get('birth_year'))
        email=post_request.get('email')
        errors={'password':[],'email':[],'birth_day':[],'birth_month':[],'birth_year':[],'birth_day':[],'username':[]}

        if birth_day <0 or birth_day>30:
            errors['birth_day'].append('Invalid Birth day')
        if birth_year<1980 or birth_year>2023:
            errors['birth_year'].append('Invalid Birth Year')
        if birth_month <0 or birth_month>12:
            errors['birth_month'].append('Invalid Birth Month')
        for er in validate_password(password,password_repeat):
            errors['password'].append(er)
        if custom_user.objects.filter(username=post_request.get('username')):
              errors['username'].append('Such username Exists!')
        if not any([x for x in errors.values() if len(x)>0]):
          email_exists = custom_user.objects.filter(email=email).exists()
          if email_exists:
              errors['email'].append('Such Email already Exists!')
          else:
              send_mail_result = Send_Email_To(template_name='User_Activation_Email.html', subject='Email Activation',
                                               contex={'act_code':act_code}, to=email)
              if send_mail_result == 'invalid':
                  errors['email'].append('Sorry!The email you entered Is Invalid!')
              elif send_mail_result=='fail':
                  errors['email'].append('Sorry!Couldnt send the email!please check your internet connection')
        return errors