from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'borrower', 'item', 'start_time','end_time','status','request_time','breakage','airdropAmount')
    fields = ('borrower', 'item', 'start_time','end_time','status','request_time','breakage')
    list_filter = ('status', 'borrower', 'item', 'start_time', 'end_time') 
admin.site.register(Order, OrderAdmin)