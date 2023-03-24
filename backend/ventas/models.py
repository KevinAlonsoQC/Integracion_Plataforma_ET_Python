from django.db import models

#models.AutoField es primaryKey
#models.CharField es de tipo String
#models.TextField es de tipo texto largo
#models.IntergerField es de tipo interger (número)

#models.ForeignKey(Class_Relacionada, on_delete=models.CASCADE)

class Continente(models.Model):
    id = models.AutoField(primary_key=True)
    continente=models.CharField(unique=True, max_length=255, verbose_name='Continente', null=False)


class Pais(models.Model):
    id = models.AutoField(primary_key=True)

    pais=models.CharField(unique=True,max_length=255, verbose_name='Pais', null=False)
    continente=models.ForeignKey(Continente, on_delete=models.CASCADE) #ForeignKey

class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)

    ciudad=models.CharField(unique=True,max_length=255, verbose_name='Ciudad', null=False)
    pais=models.ForeignKey(Pais, on_delete=models.CASCADE) #ForeignKey

class Comuna(models.Model):
    id = models.AutoField(primary_key=True)

    comuna=models.CharField(unique=True,max_length=255, verbose_name='Comuna', null=False)
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE) #ForeignKey

class Tipo_Proovedor(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_proovedor=models.CharField(max_length=255, verbose_name='Tipo_Proovedor', null=False)
    desc_tipo_proovedor=models.CharField(max_length=255, verbose_name='Descripcion', null=False)

class Tipo_Producto(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_producto=models.CharField(max_length=255, verbose_name='Tipo_Producto', null=False)
    desc_tipo_producto=models.CharField(max_length=255, verbose_name='Descripcion', null=False)

class Banco(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_banco=models.CharField(nique=True,max_length=255, verbose_name='Nombre_Banco', null=False)
    ciudad_banco=models.ForeignKey(Ciudad,on_delete=models.CASCADE, null=True)
    pais_banco=models.ForeignKey(Pais,on_delete=models.CASCADE, null=True)

class Tipo_Tarjeta(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_tarjeta=models.CharField(nique=True,max_length=255, verbose_name='Tipo_Tarjeta', null=False)
    desc_tipo_pago=models.CharField(max_length=255, verbose_name='Descripcion', null=False)
    banco=models.ForeignKey(Banco, on_delete=models.CASCADE, null=True) #ForeignKey


class Tipo_Pago(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_pago=models.CharField(nique=True,max_length=255, verbose_name='Tipo_Pago', null=False)
    desc_tipo_pago=models.CharField(max_length=255, verbose_name='Descripcion', null=False)
    tipo_tarjeta=models.ForeignKey(Tipo_Tarjeta, on_delete=models.CASCADE, null=True) #ForeignKey

class Talla_Ropa(models.Model):
    id = models.AutoField(primary_key=True)

    talla_ropa=models.CharField(nique=True,max_length=255, verbose_name='Talla_Ropa', null=False)
    desc_talla_ropa=models.CharField(max_length=255, verbose_name='Descripcion', null=False)
    medidas=models.TextField(verbose_name='Medidas_En_Cm2', null=False)

class Color(models.Model):
    id = models.AutoField(primary_key=True)

    color=models.CharField(nique=True,max_length=255, verbose_name='Color', null=False)
    rgb=models.CharField(max_length=255, verbose_name='Paleta_RGB', null=False)
    hex=models.CharField(max_length=255,verbose_name='Paleta_Hex', null=False)


class Empleado(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre=models.CharField(max_length=40, verbose_name='Nombre', null=False)
    apellido=models.CharField(max_length=40, verbose_name='Apellido', null=False)
    email=models.EmailField(unique=True, max_length=100, verbose_name='Email', null=False)
    password=models.CharField(max_length=100, verbose_name='Contraseña', null=False)

    sexo=models.CharField(max_length=1,verbose_name='Sexo', null=False) 
    celular=models.CharField(max_length=9, verbose_name='Celular', null=False) 
    edad=models.IntegerField(verbose_name='Edad', null=False) 
    
    pais=models.ForeignKey(Pais, on_delete=models.CASCADE) #ForeignKey
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE) #ForeignKey
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE) #ForeignKey

    nivel_staff=models.IntegerField(verbose_name='Nivel Staff', null=True, default=0) #ForeignKey 

class Proovedor(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre_proovedor=models.CharField(max_length=40, verbose_name='Nombre_Proovedor', null=False)
    email_proovedor=models.EmailField(unique=True, max_length=100, verbose_name='Email_Proovedor', null=False)
    celular_proovedor=models.CharField(max_length=15, verbose_name='Celular_Proovedor', null=False) 

    tipo_proovedor=models.ForeignKey(Tipo_Proovedor, on_delete=models.CASCADE, null=True) #ForeignKey
    pais=models.ForeignKey(Pais, on_delete=models.CASCADE) #ForeignKey
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE) #ForeignKey
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE) #ForeignKey

class Ventas(models.Model):
    id = models.AutoField(primary_key=True)
    
    monto_total=models.IntegerField(verbose_name='Dinero_Total_Mes', null=False)
    ganancias_totales=models.IntegerField(verbose_name='Ganancias_Mes', null=True)
    perdidas_totales=models.IntegerField(verbose_name='Perdidas_Mes', null=True)
    productos_vendidos=models.IntegerField(verbose_name='Productos_Vendidos_Mes', null=True)
    productos_devueltos=models.IntegerField(verbose_name='Productos_Devueltos_Mes', null=True)
    mes=models.DateField(auto_now_add=True, verbose_name="Datos_Mes", null=False)

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)

    tipo_categoria=models.TextField(verbose_name='Tipo_Categoria', null=True)
    desc=models.TextField(verbose_name='Descripcion', null=True)

class Sexo(models.Model):
    id = models.AutoField(primary_key=True)

    sexo=models.TextField(verbose_name='Sexo', null=True)
    desc=models.TextField(verbose_name='Descripcion', null=True)

class Edad(models.Model):
    id = models.AutoField(primary_key=True)

    rango_edad=models.CharField(verbose_name='Rango_Edad', null=True)
    desc=models.TextField(verbose_name='Descripcion', null=True)

class Producto(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_producto=models.CharField(max_length=100, verbose_name='Nombre_Producto', null=False)
    categoria_producto=models.ForeignKey(Categoria, on_delete=models.CASCADE) #ForeignKey
    sexo=models.ForeignKey(Sexo, on_delete=models.CASCADE, null=True) #ForeignKey
    edad=models.ForeignKey(Edad, on_delete=models.CASCADE, null=True) #ForeignKey


    descripcion=models.TextField(verbose_name='Descripcion', null=True)
    precio=models.IntegerField(verbose_name='Precio', null=False)

    talla_ropa=models.ForeignKey(Talla_Ropa, on_delete=models.CASCADE, null=True) #ForeignKey
    color=models.ForeignKey(Color, on_delete=models.CASCADE, null=True) #ForeignKey

class Clientes(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre=models.CharField(max_length=40, verbose_name='Nombre', null=False)
    apellido=models.CharField(max_length=40, verbose_name='Apellido', null=False)
    email=models.EmailField(unique=True, max_length=100, verbose_name='Email', null=False)
    password=models.CharField(max_length=100, verbose_name='Contraseña', null=False)

    sexo=models.CharField(max_length=1,verbose_name='Sexo', null=False) 
    celular=models.CharField(max_length=9, verbose_name='Celular', null=False) 
    edad=models.IntegerField(verbose_name='Edad', null=False) 
    
    pais=models.ForeignKey(Pais, on_delete=models.CASCADE) #ForeignKey
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE) #ForeignKey
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE) #ForeignKey


class Ordenes(models.Model):
    id = models.AutoField(primary_key=True)
    numero_orden=models.CharField(max_length=100, verbose_name='Numero_Orden', null=False)
    productos_comprados=models.CharField(max_length=100, verbose_name='Productos_Comprados', null=False)
    precio_total=models.CharField(max_length=250, verbose_name='Precio_Total', null=False)
    fecha_orden=models.DateField(auto_now_add=True, verbose_name="Fecha_Orden", null=False)

    tipo_pago=models.ForeignKey(Tipo_Pago, on_delete=models.CASCADE)  #ForeignKey
    cliente_orden=models.ForeignKey(Clientes, on_delete=models.CASCADE)#ForeignKey

class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE) #ForeignKey

    descripcion=models.TextField(verbose_name='Descripcion', null=True)
    precio=models.IntegerField(verbose_name='Precio', null=False)
    stock_disponible=models.IntegerField(verbose_name='Stock_Disponible', null=False) 
    stock_en_camino=models.IntegerField(verbose_name='Stock_En_Camino', null=False) 
    stock_en_espera=models.IntegerField(verbose_name='Stock_En_Espera', null=False) 
    stock_vendido=models.IntegerField(verbose_name='Stock_Vendido', null=False) 
    stock_devolucion=models.IntegerField(verbose_name='Stock_Devolucion', null=False) 
