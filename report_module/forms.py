from django import forms

from .models import Report,Report_Session

class Report_form(forms.ModelForm):
    class Meta:
        model=Report
        fields=['main_text','attached_file','report_session']
        labels={'main_text':'Your Report Text','attached_file':'Attach a file'}
        widgets={'main_text':forms.Textarea()}

