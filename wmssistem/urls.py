from django.urls import path
from .views import batches_relatorio, import_pdf


urlpatterns = [
    path('batches-relatorio/', batches_relatorio, name='batches_relatorio'),
    path('import-pdf/', import_pdf, name='import_pdf'),
]
