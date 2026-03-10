from django.db import models
import uuid

from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser


class BaseModel(TimeStampedModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True

# ---------------------
# Products & Categories
# ---------------------
class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ProductSpecification(BaseModel):
    product = models.ForeignKey(Product, related_name="specifications", on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    photo = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Category(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children", on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class ProductCategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'category')

# ---------------------
# Users & Contacts
# ---------------------
class AppUser(AbstractUser, BaseModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Contact(BaseModel):
    user = models.ForeignKey(AppUser, related_name="contacts", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

# ---------------------
# Stories / Blog
# ---------------------
class Story(BaseModel):
    user = models.ForeignKey(AppUser, related_name="stories", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title
