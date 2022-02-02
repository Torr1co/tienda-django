from django.urls import path
from . import views

urlpatterns = [
	path("", views.store, name="store"),
	path("carrito/", views.cart, name="cart"),
	path("caja/", views.checkout, name="checkout"),
	path("articulo_actualizado/", views.updateItem, name="update_item"),
	path("procesar_pedido/", views.processOrder, name="processOrder")
]