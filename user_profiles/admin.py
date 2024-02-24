from django.contrib import admin
from .models import SellerProfile,CustomUser


admin.site.register(SellerProfile)

@admin.register(CustomUser)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['email_or_phone','is_active',"is_seller"]
    list_filter = ["is_active",'is_seller']
    search_fields = ["is_seller"]
