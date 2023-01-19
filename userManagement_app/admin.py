from django.contrib import admin

# import Models
from .models import User


class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)