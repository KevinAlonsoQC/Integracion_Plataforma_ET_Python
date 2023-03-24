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