from django.contrib import admin
from addressbook.models import Contact,Address,PhoneNumber,Email,Website,SocialNetwork

class ContactAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'title', 'organization', 'url', 'blurb', 'profile_image']
    search_fields = ['last_name', 'first_name', 'middle_name', 'title', 'organization', 'url', 'blurb', 'profile_image']
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ['contact', 'street', 'city', 'state', 'zip', 'type']
    search_fields = ['contact', 'street', 'city', 'state', 'zip', 'type']
    
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['contact', 'phone', 'type']
    search_fields = ['contact', 'phone', 'type']
    
class EmailAdmin(admin.ModelAdmin):
    list_display = ['contact', 'email', 'type']
    search_fields = ['contact', 'email', 'type']
    
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['contact', 'website', 'type']
    search_fields = ['contact', 'website', 'type']
    
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ['contact', 'type']
    search_fields = ['contact', 'type']

admin.site.register(Contact, ContactAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)


