from django.contrib import admin
from .models import BannerDetails, BannerUploadUnSuccess, BannerTimeOver

class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_title', 'uName', 'banner_datetime']

class UnBannerUpload(admin.ModelAdmin):
    list_display = ['banner_date', 'banner_t', 'contact_no']

admin.site.register(BannerDetails, BannerAdmin)
admin.site.register(BannerUploadUnSuccess, UnBannerUpload)
admin.site.register(BannerTimeOver)