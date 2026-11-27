
import uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


# =====================================
# 1. USUARIO
# =====================================

class User(AbstractUser):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico"
    )

    is_seller = models.BooleanField(
        default=False,
        verbose_name="Es vendedor"
    )

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Código postal"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


# =====================================
# 2. CATEGORÍAS
# =====================================

class Category(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


# =====================================
# 3. PRODUCTOS
# =====================================

class Product(models.Model):

    CONDITIONS = [
        ("new", "Nuevo"),
        ("used", "Usado"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Nombre del producto"
    )

    image = models.ImageField(
    upload_to="products/",
    blank=True,
    null=True,
    verbose_name="Fotografía"
)

    description = models.TextField(
        verbose_name="Descripción"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Precio"
    )

    condition = models.CharField(
        max_length=10,
        choices=CONDITIONS,
        default="used",
        verbose_name="Estado"
    )

    stock = models.PositiveIntegerField(
        default=1,
        verbose_name="Existencias"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Vendedor"
    )

    categories = models.ManyToManyField(
        Category,
        related_name="products",
        blank=True,
        verbose_name="Categorías"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


# =====================================
# 4. CARRITO
# =====================================

class Cart(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Usuario"
    )

    products = models.ManyToManyField(
        Product,
        through="CartItem",
        related_name="carts",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Carrito de {self.user.email}"

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    @property
    def total(self):
        return sum(
            (item.subtotal for item in self.items.all()),
            Decimal("0.00")
        )


# =====================================
# 5. PRODUCTOS DEL CARRITO
# =====================================

class CartItem(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Cantidad"
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Producto del carrito"
        verbose_name_plural = "Productos del carrito"

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart"
            )
        ]
