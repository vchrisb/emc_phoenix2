from django.contrib import admin
from .models import Whiteboard

# Register your models here.
class WhiteboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'date', 'created_at']
    ordering = ['-date']
    readonly_fields = ('img_large','img_medium','img_small','img_thumb')

admin.site.register(Whiteboard, WhiteboardAdmin)
