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

        #def retrieve(self, request, *args, **kwargs):
        #    instancia = self.get_object()  # Obtener la instancia del objeto
        #    # Realizar acciones adicionales aquí antes de obtener los datos
        #    print('Modelo: ' + nombre_modelo)
        #    if nombre_modelo == 'Orden':
        #        orden = Orden.objects.filter(id=request.data.get('id')).first()
        #        detalle_orden = Detalle_Orden.objects.filter(numero_orden=orden)
        #        response.data['detalle_orden'] = detalle_orden
        #    # Llamar al método 'retrieve' del padre para obtener los datos
        #    response = super().retrieve(request, *args, **kwargs)
        #
        #    #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES, ETC
        #    print('\nObjeto obtenido\n')
        #
        #    return response


        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Los datos recibidos son válidos, podemos crear un nuevo objeto
                print('Modelo: ' + nombre_modelo)

                if nombre_modelo == 'Detalle_Orden':
                    producto = request.data.get('producto')
                    cantidad_comprada = int(request.data.get('cantidad'))
                    presencial_online = request.data.get('tipo_pedido')

                    orden = Orden.objects.filter(id=request.data.get('numero_orden')).first()
                    if not orden:
                        print('No existe esa Orden. Error con el orden ID:', request.data.get('numero_orden'))
                        return JsonResponse({'Mensaje': 'No existe esa Orden. Error con el orden ID: ' + request.data.get('numero_orden')})

                    sucursal = orden.sucursal
                    if not sucursal:
                        print('No existe la sucursal asociada a la Orden.')
                        return JsonResponse({'Mensaje': 'No existe la sucursal asociada a la Orden.'})

                    bodega = sucursal.bodega_sucursal
                    if not bodega:
                        print('No existe la bodega asociada a la sucursal.')
                        return JsonResponse({'Mensaje': 'No existe la bodega asociada a la sucursal.'})

                    inventario = Inventario.objects.filter(bodega=bodega, producto=producto)
                    inv_respaldos = Inventario.objects.filter(producto=producto)
                    cantidad_bandera = cantidad_comprada
                    
                    #Esto pasará si existe el "producto" en el inventario de la bodega.
                    if inventario.exists():
                        print('\nExiste el inventario y el producto')
                        stock_inv_original = inventario.first().stock_disponible

                        #Pasará solo si la bodega no tiene stock suficiente.
                        if cantidad_bandera > stock_inv_original:
                            cantidad_bandera -= stock_inv_original
                            for inv_r in inv_respaldos:
                                if inv_r.stock_disponible >= cantidad_bandera:
                                    print(f'\nLa bodega:{inv_r.bodega.id} tenía {inv_r.stock_disponible}. Ahora tiene: ')
                                    inv_r.stock_disponible -= cantidad_bandera
                                    print(inv_r.stock_disponible)
                                    inventario.update(stock_disponible=0)
                                    inv_r.save()
                                    self.perform_create(serializer)
                                    return JsonResponse({'Mensaje': 'Compra en camino (COD:01).'})
                                else:
                                    print(f'\nLa bodega:{inv_r.bodega.id} tenía {inv_r.stock_disponible}, ahora tendrá 0')
                                    print(inv_r.stock_disponible, cantidad_bandera)
                                    inv_r.stock_disponible = 0
                                    inv_r.save()
                                    cantidad_bandera -= inv_r.stock_disponible
                                    print('\nCantidad luego:')
                                    print(cantidad_bandera)

                            return JsonResponse({'Mensaje': 'Las bodegas no tienen suficiente stock (COD:01).'}) 
                            
                        #Pasará solo si la bodega tiene stock para la compra
                        elif cantidad_bandera <= stock_inv_original:
                            stock = stock_inv_original - cantidad_bandera
                            inventario.update(stock_disponible=stock)
                            self.perform_create(serializer)
                            return JsonResponse({'Mensaje': 'Compra en camino (COD:02).'}) 

                    #Esto pasará solo si no existe el producto dentro del "inventario" de la bodega.
                    else:
                        print('\nNo existe inventario para el producto en la bodega. Buscando en otras bodegas')
                        for inv_r in inv_respaldos:
                            if inv_r.stock_disponible >= cantidad_bandera:
                                print(f'\nLa bodega:{inv_r.bodega.id} tenía {inv_r.stock_disponible}. Ahora tiene: ')
                                inv_r.stock_disponible -= cantidad_bandera
                                print(inv_r.stock_disponible)
                                inv_r.save()
                                self.perform_create(serializer)
                                return JsonResponse({'Mensaje': 'Compra en camino (COD:03).'})
                            else:
                                print(f'\nLa bodega:{inv_r.bodega.id} tenía {inv_r.stock_disponible}, ahora tendrá 0')
                                print(inv_r.stock_disponible, cantidad_bandera)
                                inv_r.stock_disponible = 0
                                inv_r.save()
                                cantidad_bandera -= inv_r.stock_disponible
                                print('\nCantidad luego:')
                                print(cantidad_bandera)

                        return JsonResponse({'Mensaje': 'Las bodegas no tienen suficiente stock (COD:02).'})

                
                print('\nObjeto creado\n')
                self.perform_create(serializer)
                # AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES, ETC
                return JsonResponse({'Mensaje':'Ha sido creado...'})
            else:
                # Los datos recibidos no son válidos
                return JsonResponse({'Mensaje':'Datos incorrectos...'})

        def update(self, request, *args, **kwargs):
            instancia = self.get_object() #Obtener la instancia que está siendo actualizada
            # Realizar acciones adicionales aquí antes de la actualización

            # Llamar al método 'update' del padre para realizar la actualización
            # Esto actualizará los campos en la instancia con los datos proporcionados en la solicitud
            super().update(request, *args, **kwargs)

            #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
            print('\nObjeto actualizado\n')

            return JsonResponse({'Mensaje': 'Actualización exitosa'})

        def destroy(self, request, *args, **kwargs):
            instancia = self.get_object() #Obtener la instancia que se eliminará
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
