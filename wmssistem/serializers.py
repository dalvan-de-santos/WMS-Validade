from rest_framework import serializers
from.models import Supplier, Product, Batch


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Batch
        fields = ['id', 'product', 'product_id', 'lot_code', 'mfg_date', 'exp_date', 'quantity', 'created_by', 'created_at']
        