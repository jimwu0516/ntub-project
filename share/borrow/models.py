from django.db import models
from django.contrib.auth.models import User
from contribute.models import Item 
from django.utils import timezone
import random
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
        ('approve_expired', 'Approve Expired'),
        
        ('not_picked_up', 'Not Picked Up'),
        ('get_item', 'Get Item'),
        ('return_item', 'Return Item'),
        ('borrower_comment', 'Borrower Comment'),
        ('finish', 'Finish'),
    ]
    status = models.CharField(max_length=32, choices=STATUS_CHOICES) 
    BREAKAGE_CHOICES = (
            (0, '0'),
            (10, '10'),
            (20, '20'),
            (30, '30'),
            (40, '40'),
            (50, '50'),
            (60, '60'),
            (70, '70'),
            (80, '80'),
            (90, '90'),
            (100, '100'),
        )
    breakage = models.IntegerField(default=0, choices=BREAKAGE_CHOICES)
    airdropAmount = models.IntegerField(default=0)
    pin_code = models.CharField(max_length=4)

    
    objects = models.Manager() 
    
    def save(self, *args, **kwargs):
        if not self.pin_code:
            self.pin_code = self.generate_pin_code()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_pin_code():
        return str(random.randint(1000, 9999))