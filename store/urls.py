from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Autenticación
    path("registro/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    # Dashboard del vendedor
    path("dashboard/", views.dashboard, name="dashboard"),

    # CRUD de productos
    path("products/create/", views.product_create, name="product_create"),
    path("products/<uuid:pk>/edit/", views.product_update, name="product_update"),
    path("products/<uuid:pk>/delete/", views.product_delete, name="product_delete"),
]
