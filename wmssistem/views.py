from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Supplier, Product, Batch
from .serializers import SupplierSerializer, ProductSerializer, BatchSerializer
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .models import Batch
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated



# Dashboard view
@login_required
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



#Relatorios e importação PDF

@login_required
def batches_relatorio(request):
    batches = Batch.objects.all().order_by('-exp_date')
    return render(request, 'admin/batches_report.html', {'batches': batches})

@login_required
def import_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # título
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, "Relatório de Lotes")

    batches = Batch.objects.all().order_by('-exp_date')

    y = 770
    for batch in batches:
        linha = f"Código: {batch.lot_code} | Produto: {batch.product.name} | Validade: {batch.exp_date} | Qtd: {batch.quantity}"
        p.setFont("Helvetica", 10)
        p.drawString(80, y, linha)
        y -= 20
        if y < 40:
            p.showPage()
            y = 800

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="lotes.pdf")







#Classes da API
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'barcode']
    permission_classes = [IsAuthenticated]



class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['lot_code', 'product__name', 'product__barcode']
    permission_classes = [IsAuthenticated]

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
    
    

