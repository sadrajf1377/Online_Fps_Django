from django import forms
from .models import Post_Comment,Post_Model

class Comment_Form(forms.ModelForm):
    class Meta:
        model=Post_Comment
        fields=['comment_text','parent_post','written_by','parent_comment']
        labels={'comment_text':'main_text'}
        widgets={'comment_text':forms.Textarea()}


class Create_Post_Form(forms.ModelForm):
    class Meta:
        model=Post_Model
        fields=['title','caption','author']

        widgets={'caption':forms.Textarea(attrs={'style':'border:none;resize:none;border-radius:1%;box-shadow:inset 0 0 4px lightgray;'
                                                         'height:500px;width:98%;marging-left:5%','placeholder':'Write a caption for caption'}),
                 'title':forms.TextInput(attrs={'style':'border:none;resize:none;border-radius:1%;box-shadow:inset 0 0 4px lightgray;'
                                                        'height:50px;width:98%;','placeholder':'Write a title for post'})}