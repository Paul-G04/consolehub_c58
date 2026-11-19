from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .models import Product
from .forms import RegisterForm, LoginForm


# =====================================
# PÁGINA PRINCIPAL
# =====================================

def home(request):

    products = Product.objects.all().order_by("-created_at")

    context = {
        "products": products,
    }

    return render(request, "store/home.html", context)


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

            messages.success(
                request,
                "Tu cuenta fue creada correctamente."
            )

            login(request, user)

            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "store/register.html",
        {"form": form}
    )


# =====================================
# INICIO DE SESIÓN
# =====================================

class CustomLoginView(LoginView):

    template_name = "store/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


# =====================================
# CERRAR SESIÓN
# =====================================

class CustomLogoutView(LogoutView):

    next_page = "home"
