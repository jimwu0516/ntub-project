from django.contrib import admin
from .models import Item

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id','contributor', 'item_name', 'item_description','item_category', 'item_address','item_deposit_require','item_image','item_available')
    fields = ('contributor', 'item_name', 'item_description','item_category', 'item_address','item_deposit_require','item_image','item_available')
admin.site.register(Item, ItemAdmin)