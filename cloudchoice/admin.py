from django.contrib import admin

from django.contrib.auth.models import User
from cloudchoice.models import ComponentName, OS, Unit, CloudModel, Service, Vendor, Product, Plan, Component

from addressbook.models import Contact, Website, Address, Email

class ComponentNameAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class OSAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class UnitAdmin(admin.ModelAdmin):
    list_display = ['unit']
    search_fields = ['unit']

class CloudModelAdmin(admin.ModelAdmin):
    list_display = ['model', 'description']
    search_fields = ['model', 'description']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service', 'description']
    search_fields = ['service', 'description']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'website', 'address', 'email', 'phonenumber', 'socialnetwork']
    search_fields = ['name', 'contact__organization', 'website__website']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'cloudmodel', 'service', 'product_name', 'upfront']
    search_fields = ['vendor__name', 'cloudmodel__model', 'service__service', 'product_name']

class PlanAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'unit', 'unit_amount', 'unit_price']
    list_filter = ['product']
    search_fields = ['product__product_name', 'name']

class ComponentAdmin(admin.ModelAdmin):
    list_display = ['plan', 'name', 'content',  'unit', 'amount', 'price']
    list_filter = [ 'name']
    search_fields = ['plan__name', 'name__name',  'content']


admin.site.register(ComponentName, ComponentNameAdmin)
admin.site.register(OS, OSAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(CloudModel, CloudModelAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Component, ComponentAdmin)
