from django.contrib import admin

from django.contrib.auth.models import User
from panoview.models import SceneDetail, Scenes

class ScenesAdmin(admin.ModelAdmin):
    list_display = ['user', 'detail']
    search_fields = ['user__username', 'detail__textid']

class SceneDetailAdmin(admin.ModelAdmin):
    list_display = ['textid', 'name', 'width', 'height']
    search_fields = ['textid', 'name']

admin.site.register(Scenes, ScenesAdmin)
admin.site.register(SceneDetail, SceneDetailAdmin)
    
