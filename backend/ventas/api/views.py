from rest_framework import routers
from django.apps import apps
from django.db import models
from rest_framework import serializers, viewsets

def create_serializer_and_viewset(modelos):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = modelos
            fields = '__all__'

    class ViewSet(viewsets.ModelViewSet):
        queryset = modelos.objects.all()
        serializer_class = Serializer

        # Métodos adicionales de la vista aquí

    return ViewSet

def get_dynamic_viewsets():
    """
    Genera dinámicamente serializers y viewsets de DRF para todos los modelos de Django
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