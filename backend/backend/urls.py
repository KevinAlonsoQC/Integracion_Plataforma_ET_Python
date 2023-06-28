from django.contrib import admin
from django.urls import path, include
from ventas.api.views import router
from ventas import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('productos/', views.productos, name='productos'),
    path('orden_detallada/<int:id>/', views.orden_detallada, name='orden_detallada'),
    path('carga_masiva/', views.carga_masiva, name='carga_masiva'),
]
