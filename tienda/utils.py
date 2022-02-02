from . models import *
import json

def cookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	print('Carrito:', cart)
	articulos = []
	pedido = {'sacar_total_carrito':0, 'sacar_articulos_carrito':0, 'shipping': False}
	articulosCarrito = pedido['sacar_articulos_carrito']

	for i in cart:
		try:
			articulosCarrito += cart[i]["cantidad"]

			producto = Producto.objects.get(id=i)
			total = (producto.precio * cart[i]["cantidad"])

			pedido['sacar_total_carrito'] += total
			pedido['sacar_articulos_carrito'] += cart[i]["cantidad"]

			articulo = {
				'producto':{
					'id':producto.id,
					'nombre':producto.nombre,
					'precio':producto.precio,
					'imagenURL':producto.imagenURL
				},
				'cantidad':cart[i]["cantidad"],
				'sacar_total': total
			}
			articulos.append(articulo)
			pedido['shipping'] = True
		except:
			pass

	return {'articulosCarrito':articulosCarrito, 'pedido':pedido, 'articulos':articulos}

def cartData(request):
	if request.user.is_authenticated:
		cliente = request.user.cliente
		pedido, creado = Pedido.objects.get_or_create(cliente=cliente, completo=False)
		articulos = pedido.articulopedido_set.all()
		articulosCarrito = pedido.sacar_articulos_carrito
	else:
		cookieData = cookieCart(request)
		articulosCarrito = cookieData['articulosCarrito']
		pedido = cookieData['pedido']
		articulos = cookieData['articulos']

	return {'articulosCarrito':articulosCarrito, 'pedido':pedido, 'articulos':articulos}

def askOrder(request, data):
	print('Usuario no loggeado')

	print('COOKIES:', request.COOKIES)
	nombre = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)

	articulos = cookieData['articulos']

	cliente, creado = Cliente.objects.get_or_create(
		email=email,
		)
	cliente.nombre = nombre
	cliente.save()

	pedido = Pedido.objects.create(
		cliente = cliente,
		completo=False
		)
	for articulo in articulos:
		producto = Producto.objects.get(id=articulo['producto']['id'])

		articuloPedido = ArticuloPedido.objects.create(
			producto = producto,
			pedido = pedido,
			cantidad=articulo['cantidad']
			)
	return cliente, pedido