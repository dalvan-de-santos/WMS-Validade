
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wmssistem.views import SupplierViewSet, ProductViewSet, BatchViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from wmssistem.views import dashboard_view


router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)
router.register(r'batches', BatchViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
