from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Supplier, Product, Batch
from .serializers import SupplierSerializer, ProductSerializer, BatchSerializer


def dashboard_view(request):
    today = timezone.localdate()
    context = {
        "total_products": Product.objects.count(),
        "total_batches": Batch.objects.count(),
        "near_expiry": Batch.objects.filter(
            exp_date__gte=today,
            exp_date__lte=today + timezone.timedelta(days=7)
        ).count(),
        "expired": Batch.objects.filter(exp_date__lt=today).count(),
    }
    return render(request, "admin/dashboard.html", context)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'barcode']



class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['lot_code', 'product__name', 'product__barcode']


    @action(detail=False, methods=['get'])
    def expiring(self, request):
        threshold = int(request.query_params.get("days", 10))
        today = timezone.localdate()
        qs = self.queryset.filter(expiry_date__gte=today, expiry_date__lte=today + timezone.timedelta(days=threshold))
        return Response(BatchSerializer(qs, many=True).data)


    @action(detail=False, methods=['get'])
    def expired(self, request):
        today = timezone.localdate()
        qs = self.queryset.filter(expiry_date__lt=today)
        return Response(BatchSerializer(qs, many=True).data)
    
    

