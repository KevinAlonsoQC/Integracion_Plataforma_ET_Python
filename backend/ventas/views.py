import requests
from django.http import JsonResponse
from django.apps import apps
from .models import *
import json


###Primer Paso###
#En Postman, crea una nueva solicitud de tipo "POST" 
#para la URL correspondiente a tu vista de carga masiva en Django.

###Segundo Paso###
#En la sección "Body" de la solicitud en Postman, selecciona "form-data".

###Tercer Paso###
#Agrega un campo de formulario con el nombre "archivo" 
#y selecciona el archivo JSON que deseas cargar. 
#Asegurarse de seleccionar el archivo JSON que contiene los datos.
def carga_masiva(request):
    if request.method == 'POST' and 'archivo' in request.FILES:
        archivo = request.FILES['archivo']
        
        try:
            datos = json.load(archivo)
            
            # Procesar los datos y guardarlos en la base de datos
            for clave, registros in datos.items():
                if clave in apps.all_models:
                    Modelo = apps.get_model(app_label='ventas', model_name='Venta')
                    for registro in registros:
                        nombre = registro.get('nombre')
                        
                        # Verificar si el nombre ya existe en la base de datos
                        if nombre and Modelo.objects.filter(nombre=nombre).exists():
                            continue  # Si el nombre ya existe, pasa al siguiente registro
                        
                        Modelo.objects.create(**registro)
            
            return JsonResponse({'mensaje': 'Carga masiva exitosa.'})
        
        except json.JSONDecodeError:
            return JsonResponse({'mensaje': 'Error al procesar el archivo JSON.'}, status=400)
    
    return JsonResponse({'mensaje': 'Solicitud incorrecta.'}, status=400)

def home(request):
    return JsonResponse({'API': '127.0.0.1:8000/api', 'ADMIN':'127.0.0.1:8000/admin'})

#Pokemon.objects.filter(nombre=pokemon_data['name']).delete()
#def cargar_pokemons(request):
#    # Hacer una solicitud HTTP a la API de PokéAPI
#    response = requests.get('https://pokeapi.co/api/v2/pokemon/')
#    # Obtener los datos de respuesta en formato JSON
#    data = response.json()
#    #variable acumuladora de msg
#    mensaje = {}
#    # Iterar sobre los resultados y guardar los pokemons en la base de datos
#    for pokemon in data['results']:
#        # Obtener la información del pokemon a través de su URL
#        pokemon_data = requests.get(pokemon['url']).json()
#        if Pokemon.objects.filter(nombre=pokemon_data['name']).exists():
#            # El pokemon ya existe en la base de datos
#            mensaje[pokemon_data['name']] = 'El pokemon ya existe en la base de datos'
#        else:
#            # El pokemon no existe en la base de datos
#            # Crear una instancia de Pokemon y guardarla en la base de datos
#            pokemon_obj = Pokemon(
#                nombre=pokemon_data['name'],
#                altura=pokemon_data['height'],
#                peso=pokemon_data['weight'],
#                habilidades=', '.join([habilidad['ability']['name'] for habilidad in pokemon_data['abilities']])
#            )
#            pokemon_obj.save()
#            mensaje[pokemon_data['name']] = 'El pokemon fue ingresado en la base de datos'
#
#    # Crear una lista con los nombres de todos los pokemons guardados en la base de datos
#    nombres_pokemons = list(Pokemon.objects.values_list('nombre', flat=True))
#    # Devolver un JSON response con la lista de nombres de los pokemons
#    return JsonResponse({'Resultados': mensaje, 'pokemons': nombres_pokemons})
