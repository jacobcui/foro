from django.contrib import admin

from django.contrib.auth.models import User
from report.models import UserPlan as ExcelUserPlan, Plan as ExcelPlan
from mysite.models import ContactUs

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')
    search_fields = ['username', 'email']

class ExcelUserPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'option', 'expire', 'appkey', 'site')
    search_fields = ['user', 'plan']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('sender', 'subject', 'message')
    search_fields = ['sender', 'subject']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)

#admin.site.unregister(UserPlan)
admin.site.register(ExcelUserPlan, ExcelUserPlanAdmin)

