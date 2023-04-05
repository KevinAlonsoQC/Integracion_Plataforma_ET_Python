from rest_framework.viewsets import ModelViewSet
from ventas.models import *
from ventas.api.serializers import *

class postSexo(ModelViewSet):
    serializer_class = SexoSerializer
    queryset = Sexo.objects.all()

class postContinente(ModelViewSet):
    serializer_class = ContinenteSerializer
    queryset = Continente.objects.all()

class postPais(ModelViewSet):
    serializer_class = PaisSerializer
    queryset = Continente.objects.all()

class postCiudad(ModelViewSet):
    serializer_class = CiudadSerializer
    queryset = Continente.objects.all()

class postComuna(ModelViewSet):
    serializer_class = ComunaSerializer
    queryset = Continente.objects.all()