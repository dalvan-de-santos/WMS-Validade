from django.urls import path
from .views import batches_relatorio, import_pdf, near_expiry_view


urlpatterns = [
    path('batches-relatorio/', batches_relatorio, name='batches_relatorio'),
    path('near-expiry/', near_expiry_view, name='near_expiry'),
    path('import-pdf/<str:op>/', import_pdf, name='import_pdf'),
]
