from django.contrib import admin
from ventas.models import *

# Register your models here.

admin.site.register(Sexo)
admin.site.register(Continente)
admin.site.register(Pais)
admin.site.register(Ciudad)
admin.site.register(Comuna)

admin.site.register(Clientes)
admin.site.register(Empleado)