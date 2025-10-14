from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Supplier, Product, Batch
from .serializers import SupplierSerializer, ProductSerializer, BatchSerializer
from django.http import FileResponse
from .models import Batch
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO




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


def near_expiry_view(request):
    today = timezone.localdate()
    products = Batch.objects.filter(
        exp_date__gte=today,
        exp_date__lte=today + timezone.timedelta(days=10)
    ).order_by('exp_date')
    return render(request, "admin/near_expiry.html", {"products": products, "op": 'n'})



#Relatorios e importação PDF

@login_required
def batches_relatorio(request):
    batches = Batch.objects.all().order_by('-exp_date')
    return render(request, 'admin/batches_report.html', {'batches': batches, 'op': 'b'})

@login_required
def import_pdf(request, op):
    if op == 'b':
        batches = Batch.objects.all().order_by('-exp_date')
    elif op == 'n':
        today = timezone.localdate()
        batches = Batch.objects.filter(
            exp_date__gte=today,
            exp_date__lte=today + timezone.timedelta(days=10)
        ).order_by('exp_date')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Cabeçalho da tabela
    data = [["Código", "Produto", "Validade", "Quantidade"]]

    # Linhas com os dados vindos do banco
    for batch in batches:
        data.append([
            batch.lot_code,
            batch.product.name,
            batch.exp_date.strftime("%d/%m/%Y"),
            batch.quantity
        ])

    # Criar tabela
    table = Table(data, colWidths=[80, 200, 100, 80])

    # Estilo da tabela
    style = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),   # fundo do cabeçalho
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 12),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black), # bordas
    ])
    table.setStyle(style)

    # Montar documento
    elements = [table]
    doc.build(elements)

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
    
    

