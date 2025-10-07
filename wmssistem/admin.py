
from django.contrib import admin
from django.urls import path
from wmssistem.views import dashboard_view
from .models import Supplier, Product, Batch
from django.utils import timezone
from django.template.response import TemplateResponse




@admin.register(Supplier)
class SuppllierAdmin(admin.ModelAdmin):
    list_display = ('codigo_supplier', 'name')
    search_fields = ('codigo_supplier', 'name')
    ordering = ('codigo_supplier',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('codigo_product', 'name', 'supplier', 'category', 'barcode', 'unit', 'quantity')
    search_fields = ('codigo_product', 'name', 'supplier__codigo_supplier', 'category', 'unit')
    ordering = ('codigo_product',)
    list_filter = ('category', 'supplier')



@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('lot_code', 'product', 'mfg_date', 'exp_date', 'quantity', 'created_by', 'created_at')
    search_fields = ('lot_code', 'product__name', 'created_by__username')
    ordering = ('-created_at',)
