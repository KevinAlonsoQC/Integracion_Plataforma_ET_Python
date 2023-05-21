from django.apps import apps
from django.db import models
from rest_framework import serializers, viewsets, routers
from django.http import JsonResponse
from ..models import *

#ACÁ SOLO MODIFICAR LOS CREATE, DESTROY Y UPDATE DONDE DICE #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
#ACÁ SOLO MODIFICAR LOS CREATE, DESTROY Y UPDATE DONDE DICE #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
#ACÁ SOLO MODIFICAR LOS CREATE, DESTROY Y UPDATE DONDE DICE #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
#ACÁ SOLO MODIFICAR LOS CREATE, DESTROY Y UPDATE DONDE DICE #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
def create_serializer_and_viewset(modelos):
    nombre_modelo = modelos.__name__  # Obtener el nombre del modelo
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = modelos
            fields = '__all__'

    class ViewSet(viewsets.ModelViewSet):
        queryset = modelos.objects.all()
        serializer_class = Serializer

        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Los datos recibidos son válidos, podemos crear un nuevo objeto
                print('Modelo: '+nombre_modelo)

                if nombre_modelo == 'Detalle_Orden':
                    producto = request.data.get('producto')
                    for llave, valor in request.data.items():
                        if llave == 'numero_orden':
                            id_orden = Orden.objects.filter(id=valor).first()
                            if id_orden is not None:
                                sucursal = Sucursal.objects.filter(id=id_orden.sucursal.id).first()
                                if sucursal is not None:
                                    bodega = Bodega.objects.filter(id=sucursal.bodega_sucursal.id).first()
                                    if bodega is not None:
                                        inventario = Inventario.objects.filter(bodega=bodega, producto=producto)
                                        print('Existe el inventario y el producto')
                                        for stock in inventario:
                                            print('ID:', stock.id)
                                            print('Producto:', stock.producto)
                                            print('Descripción:', stock.descripcion)
                                            print('Stock Disponible:', stock.stock_disponible)
                                            print('Stock en Camino:', stock.stock_en_camino)
                                            print('Stock en Espera:', stock.stock_en_espera)
                                            print('Stock Vendido:', stock.stock_vendido)
                                            print('Stock Devolución:', stock.stock_devolucion)
                                            print('Bodega:', stock.bodega)
                                            print('------------------')

                            else:
                                print('No existe esa Orden. Error con el orden ID: '+valor)
                                return JsonResponse({'Mensaje':'No existe esa Orden. Error con el orden ID: '+valor})
                            

                    
                self.perform_create(serializer)
                print('\nObjeto creado\n')

                #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
                return JsonResponse({'Mensaje':'Ha sido creado...'})
            else:
                # Los datos recibidos no son válidos
                return JsonResponse({'Mensaje':'Datos incorrectos...'})

        def update(self, request, *args, **kwargs):
            instancia = self.get_object()  # Obtener la instancia que está siendo actualizada
            # Realizar acciones adicionales aquí antes de la actualización

            # Llamar al método 'update' del padre para realizar la actualización
            # Esto actualizará los campos en la instancia con los datos proporcionados en la solicitud
            super().update(request, *args, **kwargs)

            #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
            print('\nObjeto actualizado\n')

            return JsonResponse({'Mensaje': 'Actualización exitosa'})

        def destroy(self, request, *args, **kwargs):
            instancia = self.get_object()  # Obtener la instancia que se eliminará
            # Realizar acciones adicionales aquí antes de la eliminación

            # Llamar al método 'destroy' del padre para realizar la eliminación
            super().destroy(request, *args, **kwargs)

            #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
            print('\nObjeto eliminado\n')

            return JsonResponse({'Mensaje': 'Eliminación exitosa'})

    return ViewSet


#De acá para abajo no modificar NADA
#De acá para abajo no modificar NADA
#De acá para abajo no modificar NADA
#De acá para abajo no modificar NADA
#De acá para abajo no modificar NADA
def get_dynamic_viewsets():
    """
    Esto genera dinámicamente serializers y viewsets de DRF para todos los modelos de Django
    registrados en la aplicación, excluyendo ciertos modelos
    """
    # Lista de nombres de modelos a excluir
    excluded_models = [
        'LogEntry',
        'Permission',
        'Group',
        'User',
        'ContentType',
        'Session',
    ]
    viewsets_dict = {}
    # Iterar sobre todos los modelos de Django en la aplicación
    for model in apps.get_models():
        # Verificar que el modelo sea una subclase de django.db.models.Model
        if not issubclass(model, models.Model):
            continue
        # Excluir ciertos modelos
        if model.__name__ in excluded_models:
            continue
        # Generar un nombre de clase para el Viewset
        viewset_name = f'{model.__name__}ViewSet'
        # Crear una clase Viewset dinámica para el modelo actual
        viewset_class = create_serializer_and_viewset(model)
        # Agregar el viewset generado al diccionario de viewsets
        viewsets_dict[model.__name__.lower()] = viewset_class
    return viewsets_dict

# Obtener los viewsets dinámicamente
dynamic_viewsets = get_dynamic_viewsets()
# Registrar los viewsets en el router
router = routers.DefaultRouter()
for model_name, viewset in dynamic_viewsets.items():
    router.register(model_name, viewset)
