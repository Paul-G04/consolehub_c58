
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Category, Product, Cart, CartItem


# =====================================
# FORMULARIO DE CREACIÓN DE USUARIO
# =====================================

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = "__all__"


# =====================================
# ADMINISTRACIÓN DE USUARIOS
# =====================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "username",
        "email",
        "is_seller",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_seller",
        "is_staff",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Información de GameMarket", {
            "fields": (
                "is_seller",
                "postal_code",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "password1",
                "password2",
            ),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)


# =====================================
# ADMINISTRACIÓN DE CATEGORÍAS
# =====================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
    )

    search_fields = ("name",)


# =====================================
# ADMINISTRACIÓN DE PRODUCTOS
# =====================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "condition",
        "stock",
        "owner",
    )

    list_filter = (
        "condition",
        "categories",
    )

    search_fields = (
        "name",
        "description",
        "owner__username",
    )

    filter_horizontal = ("categories",)


# =====================================
# PRODUCTOS DEL CARRITO
# =====================================

class CartItemInline(admin.TabularInline):

    model = CartItem
    extra = 0


# =====================================
# ADMINISTRACIÓN DEL CARRITO
# =====================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart",
        "product",
        "quantity",
    )

# Register your models here.
