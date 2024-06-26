from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from Apps.TelegramAPI.models import TelegramUser, LinkKey

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'first_name', 'last_name', 'user')
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('userid', 'image_data')
    exclude = ('image_data',)


class LinkKeyAdmin(admin.ModelAdmin):
    list_display = ('token', 'username', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'token')
    readonly_fields = ('created_at',)
    
    def username(self, obj):
        if obj.user:
            url = reverse('admin:TelegramAPI_telegramuser_change', args=[obj.user.id])
            
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return None
    
    username.admin_order_field = 'username__username'


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(LinkKey, LinkKeyAdmin)