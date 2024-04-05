from django.db import models
from django.contrib.auth.models import User
from contribute.models import Item 
from django.utils import timezone
# Create your models here.

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)  
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    request_time = models.DateTimeField(default=timezone.now)

    STATUS_CHOICES = [
        ('wait_to_pay', 'Wait To Pay'),
        ('pending', 'Pending'),
        ('unpaid', 'Unpaid'),
        ('accept', 'Accept'),
        
        ('deny', 'Deny'),
        ('cancel_order', 'Cancel Order'),
        ('get_item', 'Get Item'),
        ('return_item', 'Return Item'),
        ('borrower_comment ', 'Borrower Comment'),
        ('finish', 'Finish'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES) 
    breakage = models.IntegerField(default=0, choices=[(i, str(i)) for i in range(0, 101, 10)])
    
    objects = models.Manager() 
    