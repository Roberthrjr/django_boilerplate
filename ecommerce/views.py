# Importamos la clase generics de DRF
from rest_framework import generics, status
# Importamos la clase Response de DRF
from rest_framework.response import Response
# Importamos el modelo MyUser
from ecommerce.models import MyUser
# Importamos el serializer
from .serializers import (
    ProductSerializer, 
    ProductModel, 
    ProductUpdateSerializer, 
    SaleSerializer, 
    SaleModel, 
    SaleDetailModel, 
    SaleCreateSerializer,
    UserCreateSerializer,
    MyTokenObtainPairSerializer
    )
# Importamos la libreria cloudinary
from cloudinary.uploader import upload
# Importamos el modelo User
from django.contrib.auth.models import User
# Importamos el metodo transaction
from django.db import transaction
# Importamos la clase TokenO de DRF
from rest_framework_simplejwt.views import TokenObtainPairView
# Importamos la clase environ
from os import environ
# Importamos la libreria requests
import requests
# Importamos la libreria datetime
from datetime import datetime
# Importamos la libreria pprint
from pprint import pprint

# Creamos la vista de registro para crear un nuevo usuario
class RegisterView(generics.CreateAPIView):
    # Definimos el queryset
    queryset = MyUser.objects.all()
    # Definimos el serializer
    serializer_class = UserCreateSerializer
    
    # Creamos el metodo post
    def post(self, request, *args, **kwargs):
        
        try:
            # Obtenemos el email
            email = request.data.get('email')
            # Filtramos el usuario por el email
            user = MyUser.objects.filter(email=email).first()
            # Verificamos si el usuario ya existe
            if user:
                # Retornamos la respuesta
                return Response({'message': 'El usuario ya existe'}, status = status.HTTP_400_BAD_REQUEST)
            # Creamos el usuario
            serializer = self.get_serializer(data=request.data)
            # Validamos el serializer
            serializer.is_valid(raise_exception=True)
            # Guardamos el usuario
            newUser = serializer.save()
            # Retornamos la respuesta
            response = self.serializer_class(newUser).data
            return Response(response, status = status.HTTP_201_CREATED)
                    
        except Exception as e:
            return Response({'errors': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de login para iniciar sesion
class LoginView(TokenObtainPairView):
    # Definimos el queryset
    queryset = MyUser.objects.all()
    # Definimos el serializer
    serializer_class = MyTokenObtainPairSerializer

# Creamos la vista de productos para obtener todos los productos
class ProductView(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

# Creamos la vista de productos para crear un nuevo producto
class ProductCreateView(generics.CreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

# Creamos la vista de productos para actualizar un producto
class ProductUpdateView(generics.UpdateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductUpdateSerializer

# Creamos la vista de productos para eliminar un producto
class ProductDeleteView(generics.DestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    
    # Creamos el metodo destroy
    def destroy(self, request, *args, **kwargs):
        try:
            # Obtenemos el objeto
            instance = self.get_object()
            # Actualizamos el estado del producto
            instance.status = False
            # Guardamos el objeto
            instance.save()
            # Retornamos la respuesta
            return Response({'message': 'Producto eliminado correctamente'}, status = status.HTTP_200_OK)
        except Exception as e:
            # Retornamos la respuesta
            return Response({'errors': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de productos para subir una imagen
class ProductUploadImageView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    # Creamos el metodo post 
    def post(self, request, *args, **kwargs):
        # Verificamos si el usuario esta autenticado
        try:
            # Obtenemos la imagen
            imageFile = request.FILES.get('image')
            # Verificamos si la imagen existe
            if not imageFile:
                raise Response({'message': 'No se ha facilitado ninguna imagen'})
            # Subimos la imagen
            uploadedImage = upload(imageFile)
            # Obtenemos el nombre del archivo
            imageName = uploadedImage['secure_url'].split('/')[-1]
            # Obtenemos la ruta de la imagen
            imagePath = f'{uploadedImage["resource_type"]}/{uploadedImage["type"]}/v{uploadedImage["version"]}/{imageName}'
            # Retornamos la respuesta
            return Response({'url': imagePath}, status.HTTP_200_OK)
        
        except Exception as e:
            # Retornamos la respuesta
            return Response({'errors': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de ventas para obtener todas las ventas
class SaleView(generics.ListAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer
    
# Creamos la vista de ventas para crear una venta
class SaleCreateView(generics.CreateAPIView):
    # Obtenemos el queryset
    queryset = SaleModel.objects.all()
    # Obtenemos el serializer
    serializer_class = SaleCreateSerializer
    
    @transaction.atomic
    # Creamos el metodo create
    def create(self, request, *args, **kwargs):
        try:
            # Obtenemos los datos
            data = request.data
            # Verificamos si los datos son validos
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            # Guardamos la venta
            # serializer.save()
            
            user = MyUser.objects.get(id = data['user_id'])
            
            # Guardamos la venta
            sale = SaleModel.objects.create(
                user_id = user, 
                total = data['total']
                )
            # Guardamos los detalles de la venta
            sale.save()
                        
            # Verificamos si hay stock suficiente
            for item in data['details']:
                # Obtenemos el id del producto
                productId = item['product_id']
                # Obtenemos la cantidad
                quantity = item['quantity']
                # Obtenemos el producto
                product = ProductModel.objects.get(id = productId)
                # Verificamos si hay stock suficiente
                if product.stock < quantity:
                    # Retornamos la respuesta
                    raise Exception(f'No hay stock suficiente para el producto {product.name}')
                # Actualizamos el stock
                product.stock -= quantity
                # Guardamos el producto
                product.save()
                # Creamos el detalle de la venta
                saleDetail = SaleDetailModel.objects.create(
                    product_id = product, 
                    sale_id = sale, 
                    quantity = quantity, 
                    price = item['price'], 
                    subtotal = item['subtotal']
                    )
                # Guardamos el detalle de la venta
                saleDetail.save()
            
            
            # Retornamos la respuesta            
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'errors': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de ventas para actualizar una venta
class SaleUpdateView(generics.UpdateAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer
    
# Creamos la vista de ventas para eliminar una venta
class SaleDeleteView(generics.DestroyAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer

# Creamos la vista de ventas para crear una factura
class CreateInvoiceView(generics.GenericAPIView):
    serializer_class = SaleSerializer
    
    def post(self, request):
        try:
            # Extraer la url de las variables de entorno
            url = environ.get('NUBEFACT_URL')
            token = environ.get('NUBEFACT_TOKEN')
            
            # Datos de la factura
            invoiceData = {
                'operacion': 'generar_comprobante',
                'tipo_de_comprobante': 2,
                'serie': 'BBB1',
                'numero': 1,
                'sunat_transaction': 1,
                'cliente_tipo_de_documento': 1,
                'cliente_numero_de_documento': '73201471',
                'cliente_denominacion': 'EMPRESA DE PRUEBA',
                'cliente_direccion': 'AV. LARCO 1234',
                'cliente_email': 'email@email.com',
                'fecha_de_emision': datetime.now().strftime('%d-%m-%Y'),
                'moneda': 1,
                'porcentaje_de_igv': 18.0,
                'total_gravada': 100,
                'total_igv': 18,
                'total': 118,
                'detraccion': False,
                'enviar_automaticamente_a_la_sunat': True,
                'enviar_automaticamente_al_cliente': True,
                'items': [
                    {
                        'unidad_de_medida': 'NIU',                    
                        'codigo': 'P001',
                        'codigo_producto_sunat': '10000000',
                        'descripcion': 'ZAPATILLAS NIKE',
                        'cantidad': 1,
                        'valor_unitario': 100,
                        'precio_unitario': 118,
                        'subtotal': 100,
                        'tipo_de_igv': 1,
                        'igv': 18,
                        'total': 118,
                        'anticipo_regularizacion': False
                    }
                ]
            }
            
            # Realizar la peticion
            nubeFactResponse = requests.post(url=url, headers={'Authorization': f'Bearer {token}'}, json=invoiceData)
            
            pprint(nubeFactResponse.json())
            print(nubeFactResponse.status_code)
            
            # Retornar la respuesta
            return Response({
                'message': 'Factura generada correctamente',
            }, status = status.HTTP_200_OK) 
            
        except Exception as e:
            return Response({'errors': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)