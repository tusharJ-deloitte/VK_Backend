from django.contrib import admin
from .models import BroadcastNotification

# Register your models here.
# admin.site.register(BroadcastNotification)


@admin.register(BroadcastNotification)
class BroadcastNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'broadcast_on', 'sent']
