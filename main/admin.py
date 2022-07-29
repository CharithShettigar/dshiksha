from django.contrib import admin
from main.models import User, UserTypes
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('Email', 'FirstName', 'LastName')
    list_filter = ('Email', 'FirstName', 'IsActive')
    ordering = ('-StartDate',)
    list_display = ('Email', 'FirstName', 'LastName', 'IsActive', 'is_superuser')

    # exclude = ('username',)
    
    fieldsets = (
        (None, {'fields': ('Email', 'FirstName', 'LastName', 'username')}),
        ('Permission', {'fields': ('IsActive', 'is_superuser','is_staff')}),
        ('Personal', {'fields': ("StartDate",)}),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(UserTypes)