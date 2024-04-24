# Importamos serializers de la biblioteca de rest_framework
from rest_framework import serializers
# Importamos modelos
from .models import ProductModel, SaleDetailModel, SaleModel

# Se crea la clase ProductSerializer que hereda de ModelSerializer y se define el modelo y los campos a serializar de la tabla ProductModel.
class ProductSerializer(serializers.ModelSerializer):
    # Se crea la clase Meta que hereda de ModelSerializer y se define el modelo y los campos a serializar de la tabla ProductModel.
    class Meta:
        # Se define el modelo y los campos a serializar de la tabla ProductModel.
        model = ProductModel
        fields = '__all__'
    
    # Se sobreescribe el metodo to_representation para agregar la url de la imagen al serializador.
    def to_representation(self, instance):
        # Se llama al metodo to_representation de la clase padre.
        representation = super().to_representation(instance)
        # Se agrega la url de la imagen al serializador.
        representation['image'] = instance.image.url
        # Se retorna el serializador.
        return representation

# Se crea la clase ProductUpdateSerializer que hereda de ModelSerializer y se define el modelo y los campos a serializar de la tabla ProductModel.
class ProductUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    price = serializers.FloatField(required=False)
    stock = serializers.IntegerField(required=False)
    status = serializers.BooleanField(required=False)

    class Meta:
        model = ProductModel
        fields = '__all__'

# Se crea la clase SaleDetailSerializer que hereda de ModelSerializer y se define el modelo y los campos a serializar de la tabla SaleDetailModel.
class SaleDetailSerializer(serializers.ModelSerializer):
    sale_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SaleDetailModel
        fields = '__all__'    
        
# Se crea la clase SaleSerializer que hereda de ModelSerializer y se define el modelo y los campos a serializar de la tabla SaleModel.
class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True)
    class Meta:
        model = SaleModel
        fields = '__all__'
