from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
from account.models import UserDetails


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class AccountUserDetail(UserAdmin):
    list_display = ('email', 'username', 'firstname', 'lastname')
    search_fields = ('email', 'username',)
    readonly_fields = ('email', 'username')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(UserDetails, AccountUserDetail)
