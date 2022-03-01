from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )


class Customer(BaseModel):
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    order_date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="+"
    )
    order_status = models.CharField(
        max_length=255, choices=OrderStatus.choices, default=OrderStatus.OPEN
    )
    shipping_address = models.JSONField()


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, related_name="line_items", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_name = models.CharField(max_length=255)

    @property
    def total_price(self):
        return str(self.price * self.quantity)
