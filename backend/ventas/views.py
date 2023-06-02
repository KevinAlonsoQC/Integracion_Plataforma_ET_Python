import requests
from django.http import JsonResponse
from django.apps import apps
from .models import *
import json
from django.shortcuts import render



def home(request):
    return render(request, 'template.html', {})

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
