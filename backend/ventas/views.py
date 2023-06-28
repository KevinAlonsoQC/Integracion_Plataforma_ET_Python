import requests
from django.http import JsonResponse
from django.apps import apps
from .models import *
import json
from django.shortcuts import render
from django.core import serializers
ordenes_refresh = False
ordenes_completas = {}

product_refresh = False
productos_catalogo = {}
def cargar_productos():
    global productos_catalogo
    
    producto = Producto.objects.all()
    for k in producto:
        productos_catalogo[k.id] = {}  # Crear la clave para el producto actual
        productos_catalogo[k.id]['nombre_producto'] = k.nombre_producto
    
        stock_total = 0
        detalle_producto = Inventario.objects.filter(producto=k, stock_disponible__gt=1)
        for v in detalle_producto:
            print(f'El inventario de la bodega {v.bodega.nombre_bodega} tiene {v.stock_disponible} de stock para ser comprado')
            stock_total += v.stock_disponible
    
        productos_catalogo[k.id]['stock_total'] = stock_total

    productos_catalogo = {k: v for k, v in productos_catalogo.items() if v['stock_total'] != 0}

def cargar_ordenes():
    global ordenes_completas

    ordenes_api = Orden.objects.all()
    for k in ordenes_api:
        ordenes_completas[k.id] = {}  # Crear la clave para el producto actual
        ordenes_completas[k.id]['cliente'] = k.comprador.nombre + ' ' + k.comprador.apellido
        ordenes_completas[k.id]['fecha_compra'] = k.fecha_orden
        ordenes_completas[k.id]['vendedor'] = k.vendedor.nombre + ' ' + k.vendedor.apellido

        pago_total = 0
        ordenes_completas[k.id]['detalles'] = {}
        detalle_orden = Detalle_Orden.objects.filter(numero_orden=k)

        for v in detalle_orden:
            ordenes_completas[k.id]['detalles'][v.producto.nombre_producto] = {}
            ordenes_completas[k.id]['detalles'][v.producto.nombre_producto]['cantidad'] = v.cantidad
            ordenes_completas[k.id]['detalles'][v.producto.nombre_producto]['precio_unitario'] = v.precio_unitario
            pago_total += v.precio_unitario * v.cantidad
    
        ordenes_completas[k.id]['pago_total'] = pago_total

def obtener_orden_por_id(orden_id):
    global ordenes_completas

    if orden_id in ordenes_completas:
        orden_by_id = ordenes_completas[orden_id]
        print(orden_by_id)
        return orden_by_id
    else:
        # La orden no existe
        return 'No se encontró la orden N° ' +str(orden_id)

def home(request):
    return render(request, 'template.html', {})

#Esto será llamado desde la vista de la API.
def act_productos(producto, cantidad):
    global productos_catalogo
    productos_catalogo[producto]['stock_total'] = cantidad

#Mostrará todos los productos con un stock disponible mayor a 0
def productos(request):
    global product_refresh, productos_catalogo

    if product_refresh == False:
        cargar_productos()
        product_refresh = True
        print('Cargando Productos Inicialmente')
    
    return JsonResponse({'Resultados': productos_catalogo})

def orden_detallada(request, id):
    orden_id = obtener_orden_por_id(id)
    return JsonResponse({'Resultados': orden_id})
    
def ordenes(request):   
    global ordenes_refresh, ordenes_completas
    if ordenes_refresh == False:
        cargar_ordenes()
        ordenes_refresh = True

    return JsonResponse({'Resultados': ordenes_completas})

#Pokemon.objects.filter(nombre=pokemon_data['name']).delete()
def carga_masiva(request):
    response = requests.get('https://raw.githubusercontent.com/KevinAlonsoQC/Integracion_Plataforma_ET_Python/main/backend/carga_masiva.json')
    data = response.json()
    mensaje = {}

    modelos = apps.get_models()

    # Primera etapa: insertar datos sin claves foráneas
    for clave_modelo, datos_modelo in data.items():
        if clave_modelo not in [modelo.__name__.lower() for modelo in modelos]:
            mensaje[clave_modelo] = f"El modelo '{clave_modelo}' no existe en la base de datos."
            continue
        
        modelo = next(modelo for modelo in modelos if modelo.__name__.lower() == clave_modelo)

        for item in datos_modelo:
            if not modelo._meta.get_fields(include_parents=False, include_hidden=True):
                # Si el modelo no tiene claves foráneas, insertarlo directamente
                if modelo.objects.filter(id=item['id']).exists():
                    mensaje[item['id']] = f"El objeto con ID {item['id']} ya existe en la base de datos."
                else:
                    obj = modelo(**item)
                    obj.save()
                    mensaje[item['id']] = f"El objeto con ID {item['id']} fue ingresado en la base de datos."

    # Segunda etapa: insertar datos con claves foráneas
    for clave_modelo, datos_modelo in data.items():
        if clave_modelo not in [modelo.__name__.lower() for modelo in modelos]:
            continue
        
        modelo = next(modelo for modelo in modelos if modelo.__name__.lower() == clave_modelo)

        for item in datos_modelo:
            if modelo._meta.get_fields(include_parents=False, include_hidden=True):
                # Si el modelo tiene claves foráneas, buscar las instancias referenciadas y asignarlas antes de insertar
                for campo in modelo._meta.get_fields(include_parents=False, include_hidden=True):
                    if campo.is_relation and campo.name in item:
                        relacion_modelo = campo.related_model
                        relacion_id = item.pop(campo.name)
                        relacion = relacion_modelo.objects.get(id=relacion_id)
                        item[campo.name] = relacion
                
                if modelo.objects.filter(id=item['id']).exists():
                    mensaje[item['id']] = f"El objeto con ID {item['id']} ya existe en la base de datos."
                else:
                    obj = modelo(**item)
                    obj.save()
                    mensaje[item['id']] = f"El objeto con ID {item['id']} fue ingresado en la base de datos."

    return JsonResponse({'Resultados': mensaje})
