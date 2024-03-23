from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'borrower', 'item', 'start_time','end_time','status','request_time')
    fields = ('borrower', 'item', 'start_time','end_time','status')
admin.site.register(Order, OrderAdmin)