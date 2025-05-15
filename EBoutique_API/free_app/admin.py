from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, ArchivedUser

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend the existing UserAdmin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(ArchivedUser)
class ArchivedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role','telephone',  'date_archivage')
    search_fields = ('username', 'email')
    list_filter = ('username', 'date_archivage')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'user', 'role', 'date_creation')
    search_fields = ('user__username', 'user__email')
    list_filter = ('role', 'date_creation')
