from django.contrib import admin
from .models import Asset, Ticket, Comment, InventoryItem

admin.site.register(Asset)
admin.site.register(Ticket)
admin.site.register(Comment)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'model', 'status', 'created_at')
    list_filter = ('status', 'type')
    search_fields = ('model', 'type')