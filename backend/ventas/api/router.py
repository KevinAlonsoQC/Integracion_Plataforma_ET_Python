from rest_framework.routers import DefaultRouter
from ventas.api.views import *


router_posts = DefaultRouter()

router_posts.register(prefix='sexo', basename='sexo', viewset=postSexo)
router_posts.register(prefix='continente', basename='continente', viewset=postContinente)
router_posts.register(prefix='pais', basename='pais', viewset=postPais)
router_posts.register(prefix='ciudad', basename='ciudad', viewset=postCiudad)
router_posts.register(prefix='Comuna', basename='Comuna', viewset=postComuna)