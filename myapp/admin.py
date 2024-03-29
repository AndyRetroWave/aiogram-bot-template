from django.contrib import admin
from .models import OrderModel, UserModel, UserOrderGivenModel
from django.utils.html import format_html


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'price', 'addres', 'name',
                    'phone', 'color', 'order', 'data', 'shipping_cost', 'url_link')

    def url_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.url, obj.url)

    url_link.short_description = 'URL'


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'first_name', 'last_name', 'username')


class UsersOrderGivenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'addres', 'phone', 'name')


admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(UserModel, UsersAdmin)
admin.site.register(UserOrderGivenModel, UsersOrderGivenAdmin)
