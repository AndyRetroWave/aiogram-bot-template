from .models import OrderModel, UserOrderGivenModel, UserModel
from django.utils.html import format_html
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from myapp.models import OrderModel
from myapp.resource import OrderResource



class UsersOrderGivenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'addres', 'phone', 'name')
    readonly_fields = ('user_id', 'id')


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'first_name', 'last_name', 'username')
    readonly_fields = ('user_id', 'id')

class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ('order','user_link', 'price', 'price_rub', 'addres', 'name', 'phone', 'color', 'data', 'shipping_cost')
    list_display_links = ('user_link', 'order')
    list_filter = ('data',)
    readonly_fields = ('order', 'user_id', 'id')
    search_fields = ('order','user_link', 'price', 'price_rub', 'addres', 'name', 'phone', 'color', 'data', 'shipping_cost')


admin.site.register(OrderModel, OrderAdmin)
admin.site.register(UserModel, UsersAdmin)
admin.site.register(UserOrderGivenModel, UsersOrderGivenAdmin)
