from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    Specialist,
    Scientist,
    Family,
    Genus,
    Species,
    Localization,
    Media,
    Observation,
    ObservationMedia
)

#Register your models here.
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )

admin.site.register(User)
admin.site.register(Specialist)
admin.site.register(Scientist)
admin.site.register(Family)
admin.site.register(Genus)
admin.site.register(Species)
admin.site.register(Localization)
admin.site.register(Media)
admin.site.register(Observation)
admin.site.register(ObservationMedia)