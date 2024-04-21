from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    contributor = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field='username')
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    USER_ITEM_CATEGORY= [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('sporting-goods', 'Sporting-Goods'),
        ('books, movies & music', 'Books, Movies & Music'),
        ('home & garden', 'Home & Garden'),
        ('toys & hobbies', 'Toys & Hobbies'),
        ('everything else', 'Everything Else'),
    ]
    item_category = models.CharField(
        max_length=50, choices=USER_ITEM_CATEGORY)
    item_address = models.CharField(max_length=255)
    item_deposit_require = models.DecimalField(
        max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])
    item_image = models.ImageField(upload_to='item_images/')
    item_available = models.BooleanField(default=True)
    
    objects = models.Manager() 
    


    

