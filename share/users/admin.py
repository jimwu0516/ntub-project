from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Review

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'user_place', 'airdrop_wallet_address', 'average_overdue_pick_up_time', 'average_decision_making_minute')

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

admin.site.register(Profile, ProfileAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'username', 'review_type', 'review_result', 'review_comment')
    list_filter = ('review_type', 'review_result')
    search_fields = ('username__username', 'review_comment')

admin.site.register(Review, ReviewAdmin)

