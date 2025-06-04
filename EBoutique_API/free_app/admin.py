from django.contrib import admin
from .models import (
    UserProfile,
    ArchivedUser
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'role', 'user', 'telephone', 'date_creation', 'date_maj')
    list_filter = ('role',)
    search_fields = ('user__username',)

@admin.register(ArchivedUser)
class ArchivedUserAdmin(admin.ModelAdmin):
    list_display = ('archive_par', 'date_archivage', 'raison')
    search_fields = ('archive_par__username',)
