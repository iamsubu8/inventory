from rest_framework import serializers
from apps.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Inventory
        fields='__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'