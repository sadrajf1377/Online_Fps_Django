from django.db import models
from user_moudle.models import custom_user
list_of_words=['nigga','nigger','cunt','penis','fuck','dick','negro']
# Create your models here.
class Report(models.Model):
    
    main_text=models.TextField(max_length=2000,verbose_name='main text',null=False,blank=False)
    attached_file=models.ImageField(upload_to='report_files',null=True,blank=True,verbose_name='reports attached file')
    creation_date=models.DateTimeField(auto_now_add=True,verbose_name='when was this report written')
    report_session=models.ForeignKey('Report_Session',on_delete=models.CASCADE,verbose_name='parent session',null=False,blank=False)
    reply_to=models.ForeignKey('Report',on_delete=models.CASCADE,help_text='parent message of this report',verbose_name='parent_message',null=True,
                               blank=True)
    is_reply=models.BooleanField(default=False,verbose_name='is this a reply message')
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.report_session == None:
            id=Report_Session.objects.filter(report__sent_by_id=self.sent_by.id)+1
            sess,s=Report_Session(title='New Session'+id)
            self.report_session = sess
        super().save()




class Report_Session(models.Model):
    title=models.CharField(max_length=20,verbose_name='session title',default='',null=False,blank=False)
    date_of_creation=models.DateTimeField(auto_now_add=True,blank=False,null=False,verbose_name='date of session creation')
    owner_user=models.ForeignKey(custom_user,on_delete=models.CASCADE,verbose_name='whos session is this',null=False,blank=False)