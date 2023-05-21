from django.db import models

#models.AutoField es primaryKey
#models.CharField es de tipo String
#models.TextField es de tipo texto largo
#models.IntergerField es de tipo interger (número)

#models.ForeignKey(Class_Relacionada, on_delete=models.CASCADE)
class Sexo(models.Model):
    id = models.AutoField(primary_key=True)

    sexo=models.TextField(verbose_name='Sexo', null=True)
    desc=models.TextField(verbose_name='Descripcion', null=True)

    def __str__(self):
        return self.sexo

class Continente(models.Model):
    id = models.AutoField(primary_key=True)
    continente=models.CharField(unique=True, max_length=255, verbose_name='Continente', null=False)
    def __str__(self):
        return self.continente

class Pais(models.Model):
    id = models.AutoField(primary_key=True)

    pais=models.CharField(unique=True,max_length=255, verbose_name='Pais', null=False)
    continente=models.ForeignKey(Continente, on_delete=models.CASCADE) #ForeignKey

    def __str__(self):
        return self.pais

class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)

    ciudad=models.CharField(unique=True,max_length=255, verbose_name='Ciudad', null=False)
    pais=models.ForeignKey(Pais, on_delete=models.CASCADE) #ForeignKey

    def __str__(self):
        return self.ciudad

class Comuna(models.Model):
    id = models.AutoField(primary_key=True)

    comuna=models.CharField(unique=True,max_length=255, verbose_name='Comuna', null=False)
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE) #ForeignKey

    def __str__(self):
        return self.comuna

class Tipo_Proovedor(models.Model): #6
    id = models.AutoField(primary_key=True)

    tipo_proovedor=models.CharField(max_length=255, verbose_name='Tipo_Proovedor', null=False)
    desc_tipo_proovedor=models.CharField(max_length=255, verbose_name='Descripcion', null=False)

    def __str__(self):
        return self.tipo_proovedor

class Tipo_Producto(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_producto=models.CharField(max_length=255, verbose_name='Tipo_Producto', null=False)
    desc_tipo_producto=models.CharField(max_length=255, verbose_name='Descripcion', null=False)

    def __str__(self):
        return self.tipo_producto

class Banco(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_banco=models.CharField(unique=True,max_length=255, verbose_name='Nombre_Banco', null=False)
    ciudad_banco=models.ForeignKey(Ciudad,on_delete=models.CASCADE, null=True)
    pais_banco=models.ForeignKey(Pais,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre_banco

class Tipo_Tarjeta(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_tarjeta=models.CharField(unique=True,max_length=255, verbose_name='Tipo_Tarjeta', null=False)
    desc_tipo_pago=models.CharField(max_length=255, verbose_name='Descripcion', null=False)
    banco=models.ForeignKey(Banco, on_delete=models.CASCADE, null=True) #ForeignKey

    def __str__(self):
        return self.tipo_tarjeta

class Tipo_Pago(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_pago=models.CharField(unique=True,max_length=255, verbose_name='Tipo_Pago', null=False)
    desc_tipo_pago=models.CharField(max_length=255, verbose_name='Descripcion', null=False)
    tipo_tarjeta=models.ForeignKey(Tipo_Tarjeta, on_delete=models.CASCADE, null=True) #ForeignKey

    def __str__(self):
        return self.tipo_pago

class Talla_Ropa(models.Model): #11
    id = models.AutoField(primary_key=True)

    talla_ropa=models.CharField(unique=True,max_length=255, verbose_name='Talla_Ropa', null=False)
    desc_talla_ropa=models.CharField(max_length=255, verbose_name='Descripcion', null=False)
    medidas=models.TextField(verbose_name='Medidas_En_Cm2', null=False)

    def __str__(self):
        return self.talla_ropa
    
class Color(models.Model):
    id = models.AutoField(primary_key=True)

    color=models.CharField(unique=True,max_length=255, verbose_name='Color', null=False)
    rgb=models.CharField(max_length=255, verbose_name='Paleta_RGB', null=False)
    hex=models.CharField(max_length=255,verbose_name='Paleta_Hex', null=False)
    def __str__(self):
        return self.color

class Tipo_Cuenta(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_tipo=models.CharField(unique=True,max_length=255, verbose_name='Tipo_De_Cuenta', null=False)
    desc=models.CharField(unique=True,max_length=255, verbose_name='Descripcion', null=False)
    nivel_staff=models.IntegerField(verbose_name='Nivel Staff', null=True, default=0) #ForeignKey 

    def __str__(self):
        return self.nombre_tipo

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre=models.CharField(max_length=40, verbose_name='Nombre', null=False)
    apellido=models.CharField(max_length=40, verbose_name='Apellido', null=False)
    email=models.EmailField(unique=True, max_length=100, verbose_name='Email', null=False)
    password=models.CharField(max_length=100, verbose_name='Contraseña', null=False)

    sexo=models.ForeignKey(Sexo, on_delete=models.CASCADE)
    celular=models.CharField(max_length=9, verbose_name='Celular', null=False) 
    nacimiento=models.DateField(verbose_name="Fecha_Nacimiento", null=False)

    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE) #ForeignKey
    tipo_cuenta=models.ForeignKey(Tipo_Cuenta, on_delete=models.CASCADE) #ForeignKey

    def __str__(self):
        return self.nombre+' '+self.apellido+' | Puesto: '+self.tipo_cuenta.nombre_tipo

class Clientes(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre=models.CharField(max_length=40, verbose_name='Nombre', null=False)
    apellido=models.CharField(max_length=40, verbose_name='Apellido', null=False)
    email=models.EmailField(unique=True, max_length=100, verbose_name='Email', null=False)
    password=models.CharField(max_length=100, verbose_name='Contraseña', null=False)

    sexo=models.ForeignKey(Sexo, on_delete=models.CASCADE)
    celular=models.CharField(max_length=9, verbose_name='Celular', null=False) 
    nacimiento=models.DateField(verbose_name="Fecha_Nacimiento", null=False)
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE) #ForeignKey

    def __str__(self):
        return self.nombre+' '+self.apellido

class Bodega(models.Model): #16
    id = models.AutoField(primary_key=True)

    nombre_bodega=models.CharField(unique=True,max_length=255, verbose_name='Nombre_Bodega', null=False)
    telefono=models.CharField(max_length=255,verbose_name='Telefono', null=False)
    encargado=models.ForeignKey(Empleado, on_delete=models.CASCADE)
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE) #ForeignKey

    def __str__(self):
        return self.nombre_bodega

class Sucursal(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_sucursal=models.CharField(unique=True,max_length=255, verbose_name='Nombre_Sucursal', null=False)
    telefono=models.CharField(max_length=255,verbose_name='Telefono', null=False)

    gerente=models.ForeignKey(Empleado, on_delete=models.CASCADE)
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE) #ForeignKey
    bodega_sucursal=models.ForeignKey(Bodega, on_delete=models.CASCADE) #ForeignKey

    def __str__(self):
        return self.nombre_sucursal

class Proovedor(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre_proovedor=models.CharField(max_length=40, verbose_name='Nombre_Proovedor', null=False)
    email_proovedor=models.EmailField(unique=True, max_length=100, verbose_name='Email_Proovedor', null=False)
    celular_proovedor=models.CharField(max_length=15, verbose_name='Celular_Proovedor', null=False) 

    tipo_proovedor=models.ForeignKey(Tipo_Proovedor, on_delete=models.CASCADE, null=True) #ForeignKey
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE) #ForeignKey

    def __str__(self):
        return self.nombre_proovedor

class Ventas_Mes(models.Model):
    id = models.AutoField(primary_key=True)
    
    monto_total=models.IntegerField(verbose_name='Dinero_Total_Mes', null=False)
    ganancias_totales=models.IntegerField(verbose_name='Ganancias_Mes', null=True)
    perdidas_totales=models.IntegerField(verbose_name='Perdidas_Mes', null=True)
    productos_vendidos=models.IntegerField(verbose_name='Productos_Vendidos_Mes', null=True)
    productos_devueltos=models.IntegerField(verbose_name='Productos_Devueltos_Mes', null=True)
    mes=models.DateField(auto_now_add=True, verbose_name="Datos_Mes", null=False)

    
class Promocion(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_promocion=models.CharField(max_length=255,verbose_name='Nombre_Promocion', null=False)
    desc=models.TextField(verbose_name='Descripcion', null=False)
    fecha_inicio=models.DateField(verbose_name="Fecha_Inicio", null=False)
    fecha_fin=models.DateField(verbose_name="Fecha_Fin", null=False)

    def __str__(self):
        return self.nombre_promocion


class Cupon_Descuento(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_desct=models.CharField(max_length=255,verbose_name='Nombre_Descuento', null=False)
    desc=models.TextField(verbose_name='Descripcion', null=False)
    fecha_inicio=models.DateField(verbose_name="Fecha_Inicio", null=False)
    fecha_fin=models.DateField(verbose_name="Fecha_Fin", null=False)

    def __str__(self):
        return self.nombre_desct

class Cliente_Cupon_Descuento(models.Model):
    id = models.AutoField(primary_key=True)

    cliente=models.ForeignKey(Clientes, on_delete=models.CASCADE, null=False) #ForeignKey
    cupon_descuento=models.ForeignKey(Cupon_Descuento, on_delete=models.CASCADE, null=False) #ForeignKey


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_categoria=models.TextField(verbose_name='Tipo_Categoria', null=False)
    desc=models.TextField(verbose_name='Descripcion', null=False)

    #Una serie de productos de dicha categoría pueden estar en promo
    en_promo=models.ForeignKey(Promocion, on_delete=models.CASCADE, null=True) #ForeignKey

    def __str__(self):
        return self.tipo_categoria

class Edad_Ropa(models.Model):
    id = models.AutoField(primary_key=True)

    rango_edad=models.TextField(verbose_name='Rango_Edad', null=False)
    desc=models.TextField(verbose_name='Descripcion', null=False)

    def __str__(self):
        return self.rango_edad

class Producto(models.Model): #21
    id = models.AutoField(primary_key=True)

    nombre_producto=models.CharField(max_length=100, verbose_name='Nombre_Producto', null=False)
    categoria_producto=models.ForeignKey(Categoria, on_delete=models.CASCADE) #ForeignKey
    sexo=models.ForeignKey(Sexo, on_delete=models.CASCADE, null=True) #ForeignKey
    edad_de_ropa=models.ForeignKey(Edad_Ropa, on_delete=models.CASCADE, null=True) #ForeignKey

    descripcion=models.TextField(verbose_name='Descripcion', null=True)
    precio=models.IntegerField(verbose_name='Precio', null=False)

    talla_ropa=models.ForeignKey(Talla_Ropa, on_delete=models.CASCADE, null=True) #ForeignKey
    color=models.ForeignKey(Color, on_delete=models.CASCADE, null=True) #ForeignKey

    def __str__(self):
        return self.nombre_producto
    
class Tipo_Estado(models.Model):
    id = models.AutoField(primary_key=True)

    estado=models.CharField(max_length=100, verbose_name='Tipo_Estado', null=False)
    desct=models.CharField(max_length=100, verbose_name='Descripcion', null=False)

    def __str__(self):
        return self.estado

class Tipo_Impreso(models.Model):
    id = models.AutoField(primary_key=True)

    tipo=models.CharField(max_length=100, verbose_name='Boleta_Factura', null=False)
    desct=models.CharField(max_length=100, verbose_name='Descripcion', null=False)

    def __str__(self):
        return self.tipo

class Tipo_Pedido(models.Model): #25
    id = models.AutoField(primary_key=True)

    tipo=models.CharField(max_length=100, verbose_name='Online_Presencial', null=False)
    desct=models.CharField(max_length=100, verbose_name='Descripcion', null=False)

    def __str__(self):
        return self.tipo

class Tipo_Envio(models.Model):
    id = models.AutoField(primary_key=True)

    tipo=models.CharField(max_length=100, verbose_name='Despacho_Retiro', null=False)
    desct=models.CharField(max_length=100, verbose_name='Descripcion', null=False)

    def __str__(self):
        return self.tipo

class Tipo_Hogar(models.Model):
    id = models.AutoField(primary_key=True)

    tipo=models.CharField(max_length=100, verbose_name='Casa_Depto_Otro', null=False)
    desct=models.CharField(max_length=100, verbose_name='Descripcion', null=False)

    def __str__(self):
        return self.tipo


class Direcciones_Clientes(models.Model): #28
    id = models.AutoField(primary_key=True)

    direccion=models.CharField(max_length=100, verbose_name='Direccion_Casa', null=False)
    otros=models.TextField(verbose_name='Otros', null=True)

    cliente=models.ForeignKey(Clientes, on_delete=models.CASCADE)#ForeignKey
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE)  #ForeignKey
    tipo_hogar=models.ForeignKey(Tipo_Hogar, on_delete=models.CASCADE)  #ForeignKey

    def __str__(self):
        return "Dirección: "+self.direccion+" | Cliente: "+self.cliente.nombre+" "+self.cliente.apellido



class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    numero_orden=models.CharField(max_length=100, verbose_name='Numero_Orden', null=False)
    precio_total=models.CharField(max_length=250, verbose_name='Precio_Total', null=False)
    fecha_orden=models.DateField(auto_now_add=True, verbose_name="Fecha_Orden", null=False)

    comprador=models.ForeignKey(Clientes, on_delete=models.CASCADE)#ForeignKey
    tipo_envio=models.ForeignKey(Tipo_Envio, on_delete=models.CASCADE)  #ForeignKey
    tipo_pedido=models.ForeignKey(Tipo_Pedido, on_delete=models.CASCADE)  #ForeignKey

    #Este está en NULL TRUE, porque si es retiro presencial, no debería marcar una sucursal
    direccion=models.ForeignKey(Direcciones_Clientes, on_delete=models.CASCADE, null=True)#ForeignKey
    #Este está en NULL TRUE, porque si el pago es online, no debería marcar una sucursal
    sucursal=models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True)#ForeignKey
    #Este está en NULL TRUE, porque si el pago es online, no debería marcar un vendedor
    vendedor=models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True)#ForeignKey
    
    estado=models.ForeignKey(Tipo_Estado, on_delete=models.CASCADE)  #ForeignKey
    tipo_impreso=models.ForeignKey(Tipo_Impreso, on_delete=models.CASCADE)  #ForeignKey
    tipo_pago=models.ForeignKey(Tipo_Pago, on_delete=models.CASCADE)  #ForeignKey

    def __str__(self):
        return self.numero_orden
    
class Detalle_Orden(models.Model):
    id = models.AutoField(primary_key=True)

    numero_orden=models.ForeignKey(Orden, on_delete=models.CASCADE)  #ForeignKey
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)  #ForeignKey

    cantidad=models.IntegerField(verbose_name="Cantidad_Producto", null=False)
    precio_unitario=models.IntegerField(verbose_name="Precio_Por_Unidad", null=False)
    precio_total=models.IntegerField(verbose_name="Precio_Total", null=False)
    fecha_orden=models.DateField(auto_now_add=True, verbose_name="Fecha_Orden", null=False)

    
class Inventario(models.Model): #31
    id = models.AutoField(primary_key=True)
    
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE) #ForeignKey
    descripcion=models.TextField(verbose_name='Descripcion', null=True)

    stock_disponible=models.IntegerField(verbose_name='Stock_Disponible', null=False) 
    stock_en_camino=models.IntegerField(verbose_name='Stock_En_Camino', null=False) 
    stock_en_espera=models.IntegerField(verbose_name='Stock_En_Espera', null=False) 
    stock_vendido=models.IntegerField(verbose_name='Stock_Vendido', null=False) 
    stock_devolucion=models.IntegerField(verbose_name='Stock_Devolucion', null=False) 

    bodega=models.ForeignKey(Bodega, on_delete=models.CASCADE)#ForeignKey

class Procesar_Pagos(models.Model): #31
    id = models.AutoField(primary_key=True)
    
    cliente=models.ForeignKey(Clientes, on_delete=models.CASCADE, null=False) #ForeignKey
    orden=models.ForeignKey(Orden, on_delete=models.CASCADE, null=False) #ForeignKey
    fecha_proceso=models.DateField(auto_now_add=True, verbose_name="Fecha_Procesado_Pago", null=False)

    def __str__(self):
        return self.cliente.nombre+' '+self.cliente.apellido+' | Orden: '+self.orden.numero_orden

class Recepcion_Pagos(models.Model): #31
    id = models.AutoField(primary_key=True)
    
    recepcion=models.ForeignKey(Procesar_Pagos, on_delete=models.CASCADE, null=False) #ForeignKey
    cliente=models.ForeignKey(Clientes, on_delete=models.CASCADE, null=False) #ForeignKey
    orden=models.ForeignKey(Orden, on_delete=models.CASCADE, null=False) #ForeignKey
    fecha_recepcion=models.DateField(auto_now_add=True, verbose_name="Fecha_Recepcion_Pago", null=False)

class Rechazo_Pagos(models.Model): #31
    id = models.AutoField(primary_key=True)
    
    recepcion=models.ForeignKey(Procesar_Pagos, on_delete=models.CASCADE, null=False) #ForeignKey
    cliente=models.ForeignKey(Clientes, on_delete=models.CASCADE, null=False) #ForeignKey
    orden=models.ForeignKey(Orden, on_delete=models.CASCADE, null=False) #ForeignKey
    fecha_rechazo=models.DateField(auto_now_add=True, verbose_name="Fecha_Rechazo_Pago", null=False)