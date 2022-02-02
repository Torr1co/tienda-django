from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, askOrder

def store(request):

	data = cartData(request)
	articulosCarrito = data['articulosCarrito']
	productos = Producto.objects.all()

	return render(request, "store/store.html", {
		"productos":productos,
		"articulosCarrito":articulosCarrito
		})

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	

	cliente = request.user.cliente
	producto = Producto.objects.get(id=productId)
	pedido, creado = Pedido.objects.get_or_create(cliente=cliente, completo=False)

	articuloPedido, creado = ArticuloPedido.objects.get_or_create(pedido=pedido, producto=producto)

	if action == 'add':
		articuloPedido.cantidad = (articuloPedido.cantidad + 1)
	elif action == 'remove':
		articuloPedido.cantidad = (articuloPedido.cantidad - 1)

	articuloPedido.save()

	if articuloPedido.cantidad <= 0:
		articuloPedido.delete()		


	return JsonResponse('Item was added', safe=False)

def cart(request):
	data = cartData(request)
	articulosCarrito = data['articulosCarrito']
	pedido = data['pedido']
	articulos = data['articulos']

	return render(request, "store/cart.html", {
		'articulos':articulos,
		'pedido':pedido,
		"articulosCarrito":articulosCarrito
		})

def checkout(request):
	
	data = cartData(request)
	articulosCarrito = data['articulosCarrito']
	pedido = data['pedido']
	articulos = data['articulos']

	return render(request, "store/checkout.html", {
		'articulos':articulos,
		'pedido':pedido,
		"articulosCarrito":articulosCarrito
		})

def processOrder(request):
	print('Data:', request.body)
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		cliente = request.user.cliente
		pedido, creado = Pedido.objects.get_or_create(cliente=cliente, completo=False)
		
	else:
		cliente, pedido = askOrder(request, data)

		total = float(data['form']['total'].replace(',', '.'))
		pedido.ID_de_transaccion = transaction_id
		
		if total == pedido.sacar_total_carrito:
			pedido.completo = True
		pedido.save()
		print('dou3')

		if pedido.shipping == True:
			DireccionDeEnvio.objects.create(
					cliente = cliente,
					pedido = pedido,
					direccion = data['shipping']['address'],
					ciudad = data['shipping']['city'],
					provincia = data['shipping']['state'],
					codigo_postal = data['shipping']['zipcode']
				)

	return JsonResponse('pago completo', safe=False)
