from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Supplier(models.Model):
    codigo_supplier = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999999)], verbose_name='Código do Fornecedor')
    name = models.CharField(max_length=100, unique=True, verbose_name='Nome do Fornecedor')

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return f"{self.codigo_supplier} - {self.name}"
    

class Product(models.Model):
    category_choices = [
        ('PERECIVEIS', 'Perecíveis'),
        ('NAOPERECIVEIS', 'Não Perecíveis'),
    ]
    unit_choices = [
        ('KG', 'Quilograma'),
        ('LT', 'Litro'),
        ('UN', 'Unidade'),
    ]
    codigo_product = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999999)], verbose_name="Codigo do Produto")
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do Produto")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Fornecedor")
    category = models.CharField(max_length=50, choices=category_choices, verbose_name="Categoria")
    barcode = models.CharField(max_length=13, unique=True, verbose_name="Código de Barras")
    unit = models.CharField(max_length=2, choices=unit_choices, verbose_name="Unidade")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Quantidade em Estoque")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.codigo_product} - {self.name}"
    

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto")
    lot_code = models.CharField(max_length=50, unique=True, verbose_name="Código do Lote")
    mfg_date = models.DateField(verbose_name="Data de Fabricação")
    exp_date = models.DateField(verbose_name="Data de Validade")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Quantidade no Lote")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    
        

    class Meta:
        unique_together = ('product', 'lot_code')
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"

    def days_of_expiry(self):
        from django.utils import timezone
        return (self.exp_date - timezone.localdate()).days
    
    def is_expiry(self):
        return self.days_of_expiry() <= 0
    
    def is_near_expiry(self, threshold_days=10):
        d = self.days_of_expiry()
        return 0 < d <= threshold_days

    def __str__(self):
        return f"Lote {self.lot_code} - Produto: {self.product.name}"

