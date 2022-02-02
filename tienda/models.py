from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
	usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.nombre

class Producto(models.Model):
	nombre = models.CharField(max_length=200)
	precio = models.DecimalField(max_digits=7, decimal_places=2)
	imagen = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.nombre

	@property
	def imagenURL(self):
		try:
			url = self.imagen.url
		except:
			url = ''
		return url
	

class Pedido(models.Model):
	cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.SET_NULL)
	fecha_del_pedido = models.DateTimeField(auto_now_add=True)
	completo = models.BooleanField(default=False)
	ID_de_transaccion = models.CharField(null=False, max_length=100)
	 

	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False
		articulosPedidos = self.articulopedido_set.all()
		for i in articulosPedidos:
			shipping = True
		return shipping
	

	@property
	def sacar_total_carrito(self):
		articulospedidos = self.articulopedido_set.all()
		total = sum([articulo.sacar_total for articulo in articulospedidos])
		return total

	@property
	def sacar_articulos_carrito(self):
		articulospedidos = self.articulopedido_set.all()
		total = sum([articulo.cantidad for articulo in articulospedidos])
		return total
	

class ArticuloPedido(models.Model):
	producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
	pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
	cantidad = models.IntegerField(default=0, null=True, blank=True)
	fecha_añadido = models.DateTimeField(auto_now_add=True)

	@property
	def sacar_total(self):
		total = self.producto.precio * self.cantidad
		return total
	


class DireccionDeEnvio(models.Model):
	cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
	pedido = models.ForeignKey(Pedido, null=True, on_delete=models.SET_NULL)
	direccion = models.CharField(max_length=200, null=False)
	ciudad = models.CharField(max_length=200, null=False)
	provincia = models.CharField(max_length=200, null=False)
	codigo_postal = models.CharField(max_length=200, null=False)
	fecha_añadido = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.direccion


