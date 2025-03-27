from django.contrib import admin
from .models import BannerDetails

class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_title', 'uName', 'banner_datetime']

admin.site.register(BannerDetails, BannerAdmin)