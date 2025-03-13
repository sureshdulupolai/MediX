from django.contrib import admin
from .models import Post, PostImage

# Register your models here.
class PostImageInline(admin.TabularInline):  # Display images in a tabular format
    model = PostImage
    extra = 1  # Allows adding extra images in the admin panel

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')  # Show these fields in the admin list
    search_fields = ('title',)  # Enable search by title
    inlines = [PostImageInline]  # Allows adding multiple images inside the Post admin

admin.site.register(Post, PostAdmin)
admin.site.register(PostImage) 