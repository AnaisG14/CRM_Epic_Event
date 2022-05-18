from django.contrib import admin
from .forms import UserForm
from .models import User


class UserAdmin(admin.ModelAdmin):
    form = UserForm

    list_filter = ('role', 'username')


admin.site.register(User, UserAdmin)
