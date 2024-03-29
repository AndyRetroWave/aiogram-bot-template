from django.contrib import admin
from .models import OrderModel, UserModel, UserOrderGivenModel
from django.utils.html import format_html


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id','user_link' , 'price', 'addres', 'name',
                    'phone', 'color', 'order', 'data', 'shipping_cost', 'url_link')

    def url_link(self, obj):
        url = obj.url
        link = f'<a href="{url}" target="_blank">{url}</a>'
        return format_html(link)

    url_link.short_description = 'URL'

    def user_link(self, obj):
        user_link = obj.user_link
        link = f'<a href="{user_link}" target="_blank">{user_link}</a>'
        return format_html(link)

    url_link.short_description = 'URL'


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'first_name', 'last_name', 'username')


class UsersOrderGivenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'addres', 'phone', 'name')


admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(UserModel, UsersAdmin)
admin.site.register(UserOrderGivenModel, UsersOrderGivenAdmin)
