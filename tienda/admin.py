from django.contrib import admin

from .models import *

admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(ArticuloPedido)
admin.site.register(DireccionDeEnvio)
