
from django import forms
from .models import Product_Comment
def comment_validator(value):
    forbbiden_words=['nigga','cunt','cock','pussy']
    if 'nigga' in value:
        raise ValueError('no forbidden words')
class Prdouct_Comment_Form(forms.Form):
    comment=forms.CharField(max_length=100,required=True,error_messages={'required':'please fill this field'},widget=forms.Textarea(
        attrs={'style':'border:none;border-radius:1%;background_color:transparent;color:brown'}
    ),label='Write A Comment',validators=[comment_validator])







