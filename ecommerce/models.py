# Importamos el modulo models para definir modelos de la base de datos
from django.db import models
# Importamos el modulo User para definir el modelo de usuario
from django.contrib.auth.models import User
# Importamos el modulo cloudinary para definir el modelo de imagen
from cloudinary.models import CloudinaryField

# Creamos el modelo de producto
class ProductModel(models.Model):
    # Definimos los campos del modelo
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = CloudinaryField('image')
    price = models.FloatField()
    stock = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Definimos la tabla de la base de datos
    class Meta:
        db_table = 'products'

    # Definimos el metodo __str__ para mostrar el nombre del producto
    def __str__(self):
        return self.name

# Creamos el modelo de venta
class SaleModel(models.Model):
    # Definimos los campos del modelo
    id = models.AutoField(primary_key=True)
    total = models.FloatField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # Definimos la tabla de la base de datos
    class Meta:
        db_table = 'sales'

    # Definimos el metodo __str__ para mostrar el id de la venta
    def __str__(self):
        return str(self.id)

# Creamos el modelo de detalle de venta
class SaleDetailModel(models.Model):
    # Definimos los campos del modelo
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    subtotal = models.FloatField()
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    sale_id = models.ForeignKey(SaleModel, on_delete=models.CASCADE, related_name='saleDetails')

    # Definimos la tabla de la base de datos
    class Meta:
        db_table = 'sale_details'
    
    # Definimos el metodo __str__ para mostrar el id del detalle de venta
    def __str__(self):
        return str(self.id)