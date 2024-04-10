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
    list_display = ('order', 'user_link_click', 'url_link', 'price', 'price_rub', 'color', 'data', 'shipping_cost')
    list_display_links = ('order',)
    list_filter = ('data',)
    readonly_fields = ('order', 'user_id', 'id')
    search_fields = ('order','user_link', 'url', 'price', 'price_rub', 'addres', 'name', 'phone', 'color', 'data', 'shipping_cost')

    def url_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url)
    
    url_link.short_description = "URL"
    url_link.allow_tags = True

    def user_link_click(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.user_link, obj.user_link)
    
    user_link_click.short_description = "URL"
    user_link_click.allow_tags = True

admin.site.register(OrderModel, OrderAdmin)
admin.site.register(UserModel, UsersAdmin)
admin.site.register(UserOrderGivenModel, UsersOrderGivenAdmin)
