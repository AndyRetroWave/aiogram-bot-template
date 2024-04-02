from import_export import resources
from myapp.models import OrderModel

class OrderResource(resources.ModelResource):
    class Meta:
        model = OrderModel
        fields = ('id', 'user_id', 'user_url', 'price', 'price_rub', 'addres', 'name', 'phone', 'color', 'url', 'order', 'data', 'shipping_cost')