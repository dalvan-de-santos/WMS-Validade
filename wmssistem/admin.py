from django.contrib import admin
from .models import Supplier, Product, Batch

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

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('lot_code', 'product', 'mfg_date', 'exp_date', 'quantity', 'created_by', 'created_at')
    search_fields = ('lot_code', 'product__name', 'created_by__username')
    ordering = ('-created_at',)
