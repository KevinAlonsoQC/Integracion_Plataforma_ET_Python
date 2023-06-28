from django.apps import apps
from django.db import models
from rest_framework import serializers, viewsets, routers
from django.http import JsonResponse
from ..models import *
from ..views import act_productos

#ACÁ SOLO MODIFICAR LOS CREATE, DESTROY Y UPDATE DONDE DICE #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
#ACÁ SOLO MODIFICAR LOS CREATE, DESTROY Y UPDATE DONDE DICE #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
#ACÁ SOLO MODIFICAR LOS CREATE, DESTROY Y UPDATE DONDE DICE #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
#ACÁ SOLO MODIFICAR LOS CREATE, DESTROY Y UPDATE DONDE DICE #AGREGAR VALIDACIONES ACÁ O ACTUALIZACIONES,ETC
def create_serializer_and_viewset(modelos):
    nombre_modelo = modelos.__name__  # Obtener el nombre del modelo
    
    if nombre_modelo == 'Empleado':
        class Serializer(serializers.ModelSerializer):
            class Meta:
                model = modelos
                fields = ('id', 'nombre', 'apellido', 'sexo', 'nacimiento', 'comuna', 'tipo_cuenta')   

    elif nombre_modelo == 'Detalle_Orden':
        class Serializer(serializers.ModelSerializer):
            class Meta:
                model = modelos
                fields = ('id', 'numero_orden', 'producto', 'cantidad', 'fecha_orden')  
    else:
        class Serializer(serializers.ModelSerializer):
            class Meta:
                model = modelos
                fields = '__all__'
                

    class ViewSet(viewsets.ModelViewSet):
        queryset = modelos.objects.all()
        serializer_class = Serializer

        #Esto capta los POST
        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Los datos recibidos son válidos, podemos crear un nuevo objeto
                print('Modelo: ' + nombre_modelo)

                if nombre_modelo == 'Detalle_Orden':
                    producto = request.data.get('producto')
                    cantidad_comprada = int(request.data.get('cantidad'))
                    retiro_despacho = request.data.get('tipo_envio')
                    precio_unitario = 0
                    precio_total = 0
                    
                    #ESTO DE ABAJO CAPTARÁ EL OBJETO QUE SE ESTÁ CREANDO Y LES AÑADIRÁ LOS CAMPOS FALTANTES
                    #LOS CAMPOS FALTANTES DEBEN ESTAR DECLARADOS EN EL MODELO EN models.py

                    #serializer.validated_data['precio_unitario'] = precio_unitario
                    #serializer.validated_data['precio_total'] = precio_total

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
                    

                    #Acá se obtienen las bodegas de respaldo, es decir, que si el producto no tiene stock en su bodega
                    #Recurrirá a buscar en todas las bodegas existentes para abastecer
                    inv_respaldos = Inventario.objects.filter(producto=producto)

                    estados = Tipo_Estado.objects.filter(estado='pendiente')
                    cantidad_bandera = cantidad_comprada
                    cantidad_camino = 0
                    
                    #Esto pasará si existe el "producto" en el inventario de la bodega.
                    inventario = Inventario.objects.filter(bodega=bodega, producto=producto)
                    if inventario.exists():
                        print('\nExiste el inventario y el producto')
                        stock_inv_original = inventario.first().stock_disponible
                        #Pasará solo si la bodega no tiene stock suficiente.
                        if cantidad_bandera > stock_inv_original:
                            cantidad_bandera -= stock_inv_original
                            if inv_respaldos.exists():
                                for inv_r in inv_respaldos:
                                    if inv_r.stock_disponible >= cantidad_bandera:
                                        print(f'\nLa bodega:{inv_r.bodega.id} tenía {inv_r.stock_disponible}. Ahora tiene: ')
                                        cantidad_camino += cantidad_bandera
                                        stock = inv_r.stock_disponible - cantidad_bandera
                                        inv_r.stock_disponible = stock
                                        despacho = Orden_Despacho(bodega_recepcion=bodega,bodega_emisor=inv_r.bodega,estado_despacho=estados)
                                        despacho.save()
                                        despacho_id = Inventario.objects.get(bodega_recepcion=bodega,bodega_emisor=inv_r.bodega)
                                        detalle_despacho = Detalle_Despacho(    
                                            numero_orden=despacho_id,
                                            producto=producto,
                                            cantidad=cantidad_bandera
                                        )
                                        print('Stock Final de bodega: ')
                                        print(inv_r.stock_disponible)
                                        inventario.update(stock_en_espera=stock_inv_original)
                                        inventario.update(stock_en_camino=cantidad_camino)
                                        inv_r.save()
                                        self.perform_create(serializer)
                                        return JsonResponse({'Mensaje': 'Compra en camino (COD:01).'})
                                    else:
                                        print(f'\nLa bodega:{inv_r.bodega.id} tenía {inv_r.stock_disponible}, ahora tendrá 0')
                                        print(inv_r.stock_disponible, cantidad_bandera)
                                        despacho = Orden_Despacho(bodega_recepcion=bodega,bodega_emisor=inv_r.bodega,estado_despacho=estados)
                                        despacho.save()
                                        despacho_id = Inventario.objects.get(bodega_recepcion=bodega,bodega_emisor=inv_r.bodega)
                                        detalle_despacho = Detalle_Despacho(    
                                            numero_orden=despacho_id,
                                            producto=producto,
                                            cantidad=inv_r.stock_disponible
                                        )
                                        detalle_despacho.save()
                                        cantidad_camino += inv_r.stock_disponible
                                        inv_r.stock_disponible = 0
                                        inv_r.save()
                                        cantidad_bandera -= inv_r.stock_disponible
                                        print('\nCantidad luego:')
                                        print(cantidad_bandera)
                                return JsonResponse({'Mensaje': 'Las bodegas de respaldo no tienen suficiente stock (COD:01).'}) 
                            else:
                                return JsonResponse({'Mensaje': 'Las bodegas de respaldo no tienen suficiente stock (COD:02).'}) 
                        
                        #Pasará solo si la bodega tiene stock para la compra
                        elif cantidad_bandera <= stock_inv_original:
                            stock = stock_inv_original - cantidad_bandera
                            inventario.update(stock_disponible=stock)
                            inventario.update(stock_en_espera=cantidad_comprada)
                            self.perform_create(serializer)


                    #Esto pasará solo si no existe el producto dentro del "inventario" de la bodega.
                    #Esto pasará solo si no existe el producto dentro del "inventario" de la bodega.
                    else:
                        print('\nNo existe inventario para el producto en la bodega, creandolo. Buscando en otras bodegas')
                        create_inv = Inventario(
                            producto=producto,
                            descripcion='Cantidades del producto ' + producto.nombre_producto + ' en la bodega ' + bodega.nombre_bodega,
                            stock_disponible=0,
                            stock_en_camino=0,
                            stock_en_espera=0,
                            stock_vendido=0,
                            stock_devolucion=0,
                            bodega=bodega,
                        )
                        create_inv.save()
                        inventario = Inventario.objects.filter(bodega=bodega, producto=producto)

                        if inv_respaldos.exists():
                            for inv_r in inv_respaldos:
                                if inv_r.stock_disponible >= cantidad_bandera:
                                    print(f'\nLa bodega:{inv_r.bodega.id} tenía {inv_r.stock_disponible}. Ahora tiene: ')
                                    cantidad_camino += cantidad_bandera
                                    stock = inv_r.stock_disponible - cantidad_bandera
                                    inv_r.stock_disponible = stock
                                    despacho = Orden_Despacho(bodega_recepcion=bodega,bodega_emisor=inv_r.bodega,estado_despacho=estados)
                                    despacho.save()
                                    despacho_id = Inventario.objects.get(bodega_recepcion=bodega,bodega_emisor=inv_r.bodega)
                                    detalle_despacho = Detalle_Despacho(    
                                        numero_orden=despacho_id,
                                        producto=producto,
                                        cantidad=cantidad_bandera
                                    )
                                    print('Stock Final de bodega: ')
                                    print(inv_r.stock_disponible)
                                    inventario.update(stock_en_espera=stock_inv_original)
                                    inventario.update(stock_en_camino=cantidad_camino)
                                    inv_r.save()
                                    self.perform_create(serializer)
                                    return JsonResponse({'Mensaje': 'Compra en camino (COD:03).'})
                                else:
                                    print(f'\nLa bodega:{inv_r.bodega.id} tenía {inv_r.stock_disponible}, ahora tendrá 0')
                                    print(inv_r.stock_disponible, cantidad_bandera)
                                    despacho = Orden_Despacho(bodega_recepcion=bodega,bodega_emisor=inv_r.bodega,estado_despacho=estados)
                                    despacho.save()
                                    despacho_id = Inventario.objects.get(bodega_recepcion=bodega,bodega_emisor=inv_r.bodega)
                                    detalle_despacho = Detalle_Despacho(    
                                        numero_orden=despacho_id,
                                        producto=producto,
                                        cantidad=inv_r.stock_disponible
                                    )
                                    detalle_despacho.save()
                                    cantidad_camino += inv_r.stock_disponible
                                    inv_r.stock_disponible = 0
                                    inv_r.save()
                                    cantidad_bandera -= inv_r.stock_disponible
                                    print('\nCantidad luego:')
                                    print(cantidad_bandera)
                            return JsonResponse({'Mensaje': 'Las bodegas de respaldo no tienen suficiente stock (COD:03).'})
                        else:
                            return JsonResponse({'Mensaje': 'Las bodegas de respaldo no tienen suficiente stock (COD:04).'})
                
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
            if nombre_modelo == 'Inventario':
                producto = request.data.get('producto')
                cantidad_total = request.data.get('stock_disponible')
                act_productos(producto, cantidad_total)
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
        'Sexo',
        'Continente',
        'Pais',
        'Comuna',
        'Talla_Ropa',
        'Tipo_Pago',
        'Tipo_Tarjeta',
        'Banco',
        'Tipo_Proovedor',
        'Tipo_Cuenta',
        'Proovedor',
        'Promocion',
        'Cupon_Descuento',
        'Cliente_Cupon_Descuento',
        'Categoria',
        'Edad_Ropa',
        'Tipo_Estado',
        'Tipo_Impreso',
        'Tipo_Pedido',
        'Tipo_Envio',
        'Tipo_Hogar',
        'Direcciones_Clientes',
        'Procesar_Pagos',
        'Recepcion_Pagos',
        'Rechazo_Pagos',
        'Envio_Orden',
        'Ciudad',
        'Color',
        'Ventas_Mes'
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
