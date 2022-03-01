from rest_framework import serializers
from .models import Customer, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "email"]


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["price", "quantity", "product_name", "total_price"]


class ShippingAddress(serializers.Serializer):
    street_address_1 = serializers.CharField(max_length=255, required=True)
    street_address_2 = serializers.CharField(max_length=True, allow_blank=True)
    city = serializers.CharField(max_length=255, required=True)
    state = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=3)
    zip_code = serializers.CharField(max_length=10)


from django.db.transaction import atomic


class OrderSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True)
    shipping_address = ShippingAddress()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_date",
            "customer",
            "order_status",
            "line_items",
            "shipping_address",
        ]

    @atomic
    def create(self, validated_data):
        line_items = validated_data.pop("line_items")
        order = Order.objects.create(**validated_data)
        for line_item_data in line_items:
            OrderItem.objects.create(order=order, **line_item_data)
        return order

    @atomic
    def update(self, instance, validated_data):
        line_items_data = validated_data.pop("line_items")
        OrderItem.objects.filter(order=instance).delete()
        for line_item_data in line_items_data:
            OrderItem.objects.create(order=instance, **line_item_data)
        return super().update(instance, validated_data)
