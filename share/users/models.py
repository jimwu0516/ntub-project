from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    USER_PLACE_CHOICES = [
        ('taipei', 'Taipei'),
        ('yilan', 'Yilan'),
    ]
    user_place = models.CharField(
        max_length=20, choices=USER_PLACE_CHOICES)
    airdrop_wallet_address = models.CharField(max_length=255)

    objects = models.Manager()


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    review_type = models.CharField(max_length=20, choices=[
        ('as_contributor', 'As Contributor'), ('as_borrower', 'As Borrower')])
    review_result = models.CharField(
        max_length=20, choices=[('like', 'Like'), ('dislike', 'Dislike')])
    review_comment = models.TextField()
