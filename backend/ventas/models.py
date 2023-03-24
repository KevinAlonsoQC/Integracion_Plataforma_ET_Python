from django.db import models

#AutoField es primaryKey
#CharField es de tipo String
#TextField es de tipo texto largo
#IntergerField es de tipo interger (número)

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
    
    pais=models.CharField(max_length=50,verbose_name='País', null=False) #ForeanKey
    ciudad=models.CharField(max_length=50, verbose_name='Ciudad', null=False) #ForeanKey
    comuna=models.CharField(max_length=50, verbose_name='Comuna', null=False) #ForeanKey

    nivel_staff=models.IntegerField(verbose_name='Nivel Staff', null=True, default=0) #ForeanKey 

class Proovedor(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre_proovedor=models.CharField(max_length=40, verbose_name='Nombre_Proovedor', null=False)
    email_proovedor=models.EmailField(unique=True, max_length=100, verbose_name='Email_Proovedor', null=False)
    celular_proovedor=models.CharField(max_length=15, verbose_name='Celular_Proovedor', null=False) 

    tipo_proovedor=models.IntegerField(verbose_name='Tipo_Proovedor', null=False) #ForeanKey
    pais=models.IntegerField(verbose_name='País', null=False) #ForeanKey
    ciudad=models.IntegerField(verbose_name='Ciudad', null=False) #ForeanKey
    comuna=models.IntegerField(verbose_name='Comuna', null=False) #ForeanKey

class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    
    producto=models.CharField(unique=True, max_length=100, verbose_name='Producto', null=False) #ForeanKey

    descripcion=models.TextField(verbose_name='Descripcion', null=True)
    precio=models.IntegerField(verbose_name='Precio', null=False)
    stock_disponible=models.IntegerField(verbose_name='Stock_Disponible', null=False) 
    stock_en_camino=models.IntegerField(verbose_name='Stock_En_Camino', null=False) 
    stock_en_espera=models.IntegerField(verbose_name='Stock_En_Espera', null=False) 
    stock_vendido=models.IntegerField(verbose_name='Stock_Vendido', null=False) 
    stock_devolucion=models.IntegerField(verbose_name='Stock_Devolucion', null=False) 

class Ventas(models.Model):
    id = models.AutoField(primary_key=True)
    
    monto_total=models.IntegerField(verbose_name='Dinero_Total_Mes', null=False)
    ganancias_totales=models.IntegerField(verbose_name='Ganancias_Mes', null=True)
    perdidas_totales=models.IntegerField(verbose_name='Perdidas_Mes', null=True)
    productos_vendidos=models.IntegerField(verbose_name='Productos_Vendidos_Mes', null=True)
    productos_devueltos=models.IntegerField(verbose_name='Productos_Devueltos_Mes', null=True)
    mes=models.DateField(verbose_name="Datos_Mes", null=False)

class Producto(models.Model):
    id = models.AutoField(primary_key=True)

    nombre=models.CharField(max_length=100, verbose_name='Nombre', null=False)
    descripcion=models.TextField(verbose_name='Descripcion', null=True)
    precio=models.IntegerField(verbose_name='Precio', null=False)
    talla=models.CharField(max_length=10, verbose_name='Talla', null=False)
    color=models.CharField(max_length=20, verbose_name='Color', null=False)
class Categorías(models.Model):
    id = models.AutoField(primary_key=True)

    r_mujer=models.TextField(verbose_name='Ropa para mujer', null=True)
    r_hombre=models.TextField(verbose_name='Ropa para hombre', null=True)
    r_niño=models.TextField(verbose_name='Ropa para niño', null=True)
    calzado=models.CharField(max_length=10, verbose_name='Calzado', null=False)
    accesorios=models.TextField(verbose_name='Accesorios', null=True)
class Clientes(models.Model):
    id = models.AutoField(primary_key=True)

    nombre=models.CharField(max_length=50, verbose_name='Nombre', null=False)
    direccion=models.CharField(max_length=50, verbose_name='Dirección', null=False)
    numero=models.CharField(max_length=11, verbose_name='Numero', null=False)
    correo=models.CharField(max_length=100, verbose_name='Correo', null=False)
class Ordenes(models.Model):
    id = models.AutoField(primary_key=True)

    F_orden=models.TextField(verbose_name='Fecha de orden', null=True)
    N_orden=models.CharField(max_length=100, verbose_name='Numero de orden', null=False)
    C_orden=models.TextField(verbose_name='Cliente que realizo la orden', null=False)
    P_comprados=models.CharField(max_length=100, verbose_name='Productos comprados', null=False)
    Precio_total=models.CharField(max_length=250, verbose_name='Precio total', null=False)
    MD_pago=models.CharField(max_length=30, verbose_name='Metodo de pago', null=False)