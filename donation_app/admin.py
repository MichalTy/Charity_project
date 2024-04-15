from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Donation, Institution, Category


class CustomUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
            return False
        return super().has_delete_permission(request, obj)

    def delete_model(self, request, obj):
        if obj == request.user:
            return
        super().delete_model(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Donation)
admin.site.register(Institution)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
