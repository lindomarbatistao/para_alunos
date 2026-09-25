from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'imoveis', ImovelViewSet, basename='imoveis')
router.register(r'pagamentos', PagamentoViewSet, basename='pagamentos')
router.register(r'contratos', ContratoViewSet, basename='contratos')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", RegisterView.as_view(), name="register"),
    # path('importar_imoveis/', importar_imoveis),
    path('', include(router.urls)),
]