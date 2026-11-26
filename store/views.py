from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseForbidden

from .models import Product
from .forms import RegisterForm, LoginForm, ProductForm


# =====================================
# INICIO
# =====================================

def home(request):
    products = Product.objects.all().order_by("-created_at")

    return render(request, "store/home.html", {
        "products": products
    })


# =====================================
# REGISTRO
# =====================================

def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Tu cuenta fue creada correctamente.")
            return redirect("dashboard" if user.is_seller else "home")
    else:
        form = RegisterForm()

    return render(request, "store/register.html", {
        "form": form
    })


# =====================================
# LOGIN
# =====================================

class CustomLoginView(LoginView):
    template_name = "store/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_seller:
            return "/dashboard/"
        return "/"


# =====================================
# LOGOUT
# =====================================

class CustomLogoutView(LogoutView):
    next_page = "home"


# =====================================
# DASHBOARD DEL VENDEDOR
# =====================================

@login_required
def dashboard(request):
    if not request.user.is_seller:
        return HttpResponseForbidden(
            "No tienes permisos para acceder al panel de vendedor."
        )

    products = Product.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    # Calcula la suma total del stock para mostrarla en la tarjeta del dashboard
    total_stock = products.aggregate(total=Sum("stock"))["total"] or 0

    return render(request, "store/dashboard.html", {
        "products": products,
        "total_products": products.count(),
        "total_stock": total_stock
    })


# =====================================
# CREAR PRODUCTO
# =====================================

@login_required
def product_create(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("Solo los vendedores pueden publicar.")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            form.save_m2m()

            messages.success(request, "¡Tu producto fue publicado correctamente!")
            return redirect("dashboard")
    else:
        form = ProductForm()

    return render(request, "store/product_form.html", {
        "form": form,
        "title": "Publicar producto",
        "button_text": "Publicar producto"
    })


# =====================================
# EDITAR PRODUCTO
# =====================================

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.owner != request.user:
        return HttpResponseForbidden(
            "No puedes modificar productos de otro vendedor."
        )

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("dashboard")
    else:
        form = ProductForm(instance=product)

    return render(request, "store/product_form.html", {
        "form": form,
        "title": "Editar producto",
        "button_text": "Guardar cambios"
    })


# =====================================
# ELIMINAR PRODUCTO
# =====================================

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.owner != request.user:
        return HttpResponseForbidden(
            "No puedes eliminar productos de otro vendedor."
        )

    if request.method == "POST":
        product.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("dashboard")

    return render(request, "store/product_confirm_delete.html", {
        "product": product
    })
