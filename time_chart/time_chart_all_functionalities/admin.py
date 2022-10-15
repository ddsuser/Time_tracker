from django.contrib import admin
from .models import user_entry , user_feedback , user_settings , user_status


class user_settingsAdmin(admin.ModelAdmin):

    list_display = ('user','fiscal_year_start_date','annual_billing_target_in_hours','user_worked_time','performance')
    list_filter = (('fiscal_year_start_date', admin.EmptyFieldListFilter),'fiscal_year_start_date',)

class user_feedbackAdmin(admin.ModelAdmin):

    list_display = ('user','short_feedback','date_time')

    def short_feedback(self,obj):
        return obj.feedback[:30]

class user_entryAdmin(admin.ModelAdmin):

    list_display = ('user','entry_date','work_time','short_desc','category')
    list_filter = ('category','entry_date',)

    def short_desc(self,obj):
        return obj.desc[:30]

class user_statusAdmin(admin.ModelAdmin):

    list_display = ('user','status_now')
    list_filter = ('status_now',)
    search_fields = ['status_now']


admin.site.register(user_settings,user_settingsAdmin)
admin.site.register(user_feedback,user_feedbackAdmin)
admin.site.register(user_entry,user_entryAdmin)
admin.site.register(user_status,user_statusAdmin)


