from django.contrib import admin
from .models import User, Post, Relationship, Like

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "date_joined", "email")

class PostAdmin(admin.ModelAdmin):
    list_display = ("poster","pk", "content")

class RelationshipAdmin(admin.ModelAdmin):
    list_display = ("from_user","to_user")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("post","user")
   
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Relationship,RelationshipAdmin)
admin.site.register(Like, LikeAdmin)