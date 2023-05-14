# Generated by Django 4.0.3 on 2023-05-11 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_banco', models.CharField(max_length=255, unique=True, verbose_name='Nombre_Banco')),
            ],
        ),
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_bodega', models.CharField(max_length=255, unique=True, verbose_name='Nombre_Bodega')),
                ('telefono', models.CharField(max_length=255, verbose_name='Telefono')),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_categoria', models.TextField(verbose_name='Tipo_Categoria')),
                ('desc', models.TextField(verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ciudad', models.CharField(max_length=255, unique=True, verbose_name='Ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_unico', models.CharField(max_length=100, unique=True, verbose_name='Nombre_Unico')),
                ('nombre', models.CharField(max_length=40, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=40, verbose_name='Apellido')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email')),
                ('password', models.CharField(max_length=100, verbose_name='Contraseña')),
                ('celular', models.CharField(max_length=9, verbose_name='Celular')),
                ('nacimiento', models.DateField(verbose_name='Fecha_Nacimiento')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('color', models.CharField(max_length=255, unique=True, verbose_name='Color')),
                ('rgb', models.CharField(max_length=255, verbose_name='Paleta_RGB')),
                ('hex', models.CharField(max_length=255, verbose_name='Paleta_Hex')),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comuna', models.CharField(max_length=255, unique=True, verbose_name='Comuna')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Continente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('continente', models.CharField(max_length=255, unique=True, verbose_name='Continente')),
            ],
        ),
        migrations.CreateModel(
            name='Cupon_Descuento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_desct', models.CharField(max_length=255, verbose_name='Nombre_Descuento')),
                ('desc', models.TextField(verbose_name='Descripcion')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha_Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha_Fin')),
            ],
        ),
        migrations.CreateModel(
            name='Direcciones_Clientes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('direccion', models.CharField(max_length=100, verbose_name='Direccion_Casa')),
                ('otros', models.TextField(null=True, verbose_name='Otros')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.clientes')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.comuna')),
            ],
        ),
        migrations.CreateModel(
            name='Edad_Ropa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rango_edad', models.TextField(verbose_name='Rango_Edad')),
                ('desc', models.TextField(verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_unico', models.CharField(max_length=100, unique=True, verbose_name='Nombre_Unico')),
                ('nombre', models.CharField(max_length=40, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=40, verbose_name='Apellido')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email')),
                ('password', models.CharField(max_length=100, verbose_name='Contraseña')),
                ('celular', models.CharField(max_length=9, verbose_name='Celular')),
                ('nacimiento', models.DateField(verbose_name='Fecha_Nacimiento')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.comuna')),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero_orden', models.CharField(max_length=100, verbose_name='Numero_Orden')),
                ('precio_total', models.CharField(max_length=250, verbose_name='Precio_Total')),
                ('fecha_orden', models.DateField(auto_now_add=True, verbose_name='Fecha_Orden')),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.clientes')),
                ('direccion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.direcciones_clientes')),
            ],
        ),
        migrations.CreateModel(
            name='Procesar_Pago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_proceso', models.DateField(auto_now_add=True, verbose_name='Fecha_Procesado_Pago')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.clientes')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.orden')),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_promocion', models.CharField(max_length=255, verbose_name='Nombre_Promocion')),
                ('desc', models.TextField(verbose_name='Descripcion')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha_Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha_Fin')),
            ],
        ),
        migrations.CreateModel(
            name='Sexo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sexo', models.TextField(null=True, verbose_name='Sexo')),
                ('desc', models.TextField(null=True, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Talla_Ropa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('talla_ropa', models.CharField(max_length=255, unique=True, verbose_name='Talla_Ropa')),
                ('desc_talla_ropa', models.CharField(max_length=255, verbose_name='Descripcion')),
                ('medidas', models.TextField(verbose_name='Medidas_En_Cm2')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Cuenta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo', models.CharField(max_length=255, unique=True, verbose_name='Tipo_De_Cuenta')),
                ('desc', models.CharField(max_length=255, unique=True, verbose_name='Descripcion')),
                ('nivel_staff', models.IntegerField(default=0, null=True, verbose_name='Nivel Staff')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Envio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=100, verbose_name='Despacho_Retiro')),
                ('desct', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Estado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(max_length=100, verbose_name='Tipo_Estado')),
                ('desct', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Hogar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=100, verbose_name='Casa_Depto_Otro')),
                ('desct', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Impreso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=100, verbose_name='Boleta_Factura')),
                ('desct', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Pedido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=100, verbose_name='Online_Presencial')),
                ('desct', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_producto', models.CharField(max_length=255, verbose_name='Tipo_Producto')),
                ('desc_tipo_producto', models.CharField(max_length=255, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Proovedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_proovedor', models.CharField(max_length=255, verbose_name='Tipo_Proovedor')),
                ('desc_tipo_proovedor', models.CharField(max_length=255, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Ventas_Mes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('monto_total', models.IntegerField(verbose_name='Dinero_Total_Mes')),
                ('ganancias_totales', models.IntegerField(null=True, verbose_name='Ganancias_Mes')),
                ('perdidas_totales', models.IntegerField(null=True, verbose_name='Perdidas_Mes')),
                ('productos_vendidos', models.IntegerField(null=True, verbose_name='Productos_Vendidos_Mes')),
                ('productos_devueltos', models.IntegerField(null=True, verbose_name='Productos_Devueltos_Mes')),
                ('mes', models.DateField(auto_now_add=True, verbose_name='Datos_Mes')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Tarjeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_tarjeta', models.CharField(max_length=255, unique=True, verbose_name='Tipo_Tarjeta')),
                ('desc_tipo_pago', models.CharField(max_length=255, verbose_name='Descripcion')),
                ('banco', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.banco')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Pago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_pago', models.CharField(max_length=255, unique=True, verbose_name='Tipo_Pago')),
                ('desc_tipo_pago', models.CharField(max_length=255, verbose_name='Descripcion')),
                ('tipo_tarjeta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_tarjeta')),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_sucursal', models.CharField(max_length=255, unique=True, verbose_name='Nombre_Sucursal')),
                ('telefono', models.CharField(max_length=255, verbose_name='Telefono')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.comuna')),
                ('gerente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Rechazo_Pago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_rechazo', models.DateField(auto_now_add=True, verbose_name='Fecha_Rechazo_Pago')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.clientes')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.orden')),
                ('recepcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.procesar_pago')),
            ],
        ),
        migrations.CreateModel(
            name='Recepcion_Pago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_recepcion', models.DateField(auto_now_add=True, verbose_name='Fecha_Recepcion_Pago')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.clientes')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.orden')),
                ('recepcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.procesar_pago')),
            ],
        ),
        migrations.CreateModel(
            name='Proovedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_unico', models.CharField(max_length=100, unique=True, verbose_name='Nombre_Unico')),
                ('nombre_proovedor', models.CharField(max_length=40, verbose_name='Nombre_Proovedor')),
                ('email_proovedor', models.EmailField(max_length=100, unique=True, verbose_name='Email_Proovedor')),
                ('celular_proovedor', models.CharField(max_length=15, verbose_name='Celular_Proovedor')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.comuna')),
                ('tipo_proovedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_proovedor')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=100, verbose_name='Nombre_Producto')),
                ('descripcion', models.TextField(null=True, verbose_name='Descripcion')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('categoria_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.categoria')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.color')),
                ('edad_de_ropa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.edad_ropa')),
                ('sexo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.sexo')),
                ('talla_ropa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.talla_ropa')),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pais', models.CharField(max_length=255, unique=True, verbose_name='Pais')),
                ('continente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.continente')),
            ],
        ),
        migrations.AddField(
            model_name='orden',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_estado'),
        ),
        migrations.AddField(
            model_name='orden',
            name='sucursal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.sucursal'),
        ),
        migrations.AddField(
            model_name='orden',
            name='tipo_envio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_envio'),
        ),
        migrations.AddField(
            model_name='orden',
            name='tipo_impreso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_impreso'),
        ),
        migrations.AddField(
            model_name='orden',
            name='tipo_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_pago'),
        ),
        migrations.AddField(
            model_name='orden',
            name='tipo_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_pedido'),
        ),
        migrations.AddField(
            model_name='orden',
            name='vendedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.empleado'),
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField(null=True, verbose_name='Descripcion')),
                ('stock_disponible', models.IntegerField(verbose_name='Stock_Disponible')),
                ('stock_en_camino', models.IntegerField(verbose_name='Stock_En_Camino')),
                ('stock_en_espera', models.IntegerField(verbose_name='Stock_En_Espera')),
                ('stock_vendido', models.IntegerField(verbose_name='Stock_Vendido')),
                ('stock_devolucion', models.IntegerField(verbose_name='Stock_Devolucion')),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.bodega')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.producto')),
            ],
        ),
        migrations.AddField(
            model_name='empleado',
            name='sexo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.sexo'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='tipo_cuenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_cuenta'),
        ),
        migrations.AddField(
            model_name='direcciones_clientes',
            name='tipo_hogar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.tipo_hogar'),
        ),
        migrations.CreateModel(
            name='Detalle_Orden',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(verbose_name='Cantidad_Producto')),
                ('precio_unitario', models.IntegerField(verbose_name='Precio_Por_Unidad')),
                ('precio_total', models.IntegerField(verbose_name='Precio_Total')),
                ('fecha_orden', models.DateField(auto_now_add=True, verbose_name='Fecha_Orden')),
                ('numero_orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.orden')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.producto')),
            ],
        ),
        migrations.AddField(
            model_name='clientes',
            name='comuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.comuna'),
        ),
        migrations.AddField(
            model_name='clientes',
            name='sexo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.sexo'),
        ),
        migrations.CreateModel(
            name='Cliente_Cupon_Descuento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.clientes')),
                ('cupon_descuento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.cupon_descuento')),
            ],
        ),
        migrations.AddField(
            model_name='ciudad',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.pais'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='en_promo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.promocion'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='comuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.comuna'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='encargado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.empleado'),
        ),
        migrations.AddField(
            model_name='banco',
            name='ciudad_banco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.ciudad'),
        ),
        migrations.AddField(
            model_name='banco',
            name='pais_banco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.pais'),
        ),
    ]
