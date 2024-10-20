from django.contrib import admin
from .models import Report,Report_Session
# Register your models here.
class settings(admin.ModelAdmin):
    list_display = ['id','main_text','creation_date','report_session','reply_to','is_reply']

admin.site.register(Report,settings)
admin.site.register(Report_Session)