import requests
from django.http import JsonResponse
from django.apps import apps
from .models import *
import json
from django.shortcuts import render
from django.core import serializers

#Esto causa error cuando se hacen migraciones, a excepcion de eso, funciona correctamente.
productos_catalogo = {}
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

def home(request):
    return render(request, 'template.html', {})

def act_productos(producto, cantidad):
    productos_catalogo[producto]['stock_total'] = cantidad

#Mostrará todos los productos con un stock disponible mayor a 0
def productos(request):
    return JsonResponse({'Resultados': productos_catalogo})

def orden_detallada(request, id):
    mensaje = {}
    orden = Orden.objects.filter(id=id).first()
    detalle_orden = Detalle_Orden.objects.filter(numero_orden=orden)

    serialized_orden = serializers.serialize('json', [orden])
    serialized_detalle_orden = serializers.serialize('json', detalle_orden)

    mensaje['orden'] = serialized_orden
    mensaje['detalle_orden'] = serialized_detalle_orden

    return JsonResponse({'Resultados': mensaje})
    
def ordenes(request):
    mensaje = {}
    ordenes = Orden.objects.all()
    mensaje['ordenes'] = []
    
    for orden in ordenes:
        detalle_orden = Detalle_Orden.objects.filter(numero_orden=orden)
        serialized_orden = serializers.serialize('json', [orden])
        serialized_detalle_orden = serializers.serialize('json', detalle_orden)
        mensaje['ordenes'].append({
            'orden': serialized_orden,
            'detalle_orden': serialized_detalle_orden
        })

    
    return JsonResponse({'Resultados': mensaje})

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
