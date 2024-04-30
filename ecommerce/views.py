# Importamos la clase generics de DRF
from rest_framework import generics, status
# Importamos la clase APIView de DRF
from rest_framework.views import APIView 
# Importamos la clase Response de DRF
from rest_framework.response import Response
# Importamos la clase Request de DRF
from rest_framework.request import Request
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
# Importamos la libreria mercadopago
import mercadopago

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
            
           
            items = []
                        
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
                
                descripcion = product.name
                valor_unitario = product.price
                cantidad = quantity
                igv = item['subtotal'] * 0.18
                print(igv)
                precio_unitario = (item['price']) + (igv/cantidad)
                print(precio_unitario)
                total = data['total']
                
                items.append({
                    'unidad_de_medida': 'NIU',                    
                    'codigo': 'P001',
                    'codigo_producto_sunat': '10000000',
                    'descripcion': descripcion,
                    'cantidad': cantidad,
                    'valor_unitario': valor_unitario,
                    'precio_unitario': precio_unitario,
                    'subtotal': item['subtotal'],
                    'tipo_de_igv': 1,
                    'igv': 18,
                    'total': total,
                    'anticipo_regularizacion': False
                })
            
            body = {
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
                'total_gravada': item['subtotal'],
                'total_igv': igv,
                'total': total,
                'detraccion': False,
                'enviar_automaticamente_a_la_sunat': True,
                'enviar_automaticamente_al_cliente': True,
                'items': items
            }
            
            # Generamos la factura
            nubeFactResponse = requests.post(
                url=environ.get('NUBEFACT_URL'), 
                headers={
                    'Authorization': f'Bearer {environ.get("NUBEFACT_TOKEN")}'
                    }, 
                json=body
            )
            
            # Verificamos si la respuesta es correcta
            json = nubeFactResponse.json()
            if nubeFactResponse.status_code != 200:
                raise Exception(json['errors'])
            
            # Retornamos la respuesta            
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        except Exception as e:
            # Deshacemos la transaccion
            transaction.set_rollback(True)
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
            # nubeFactResponse = requests.post(url=url, headers={'Authorization': f'Bearer {token}'}, json=invoiceData)
            nubeFactResponse = requests.post(url=url, headers={'Authorization': f'Bearer {token}'}, json=invoiceData)
            
            # Obtener el json de la respuesta
            json = nubeFactResponse.json()
            
            # Verificar si la respuesta es correcta
            if nubeFactResponse.status_code != 200:
                raise Exception(json['errors'])
            
            # Retornar la respuesta
            return Response({
                'message': 'Comprobante generado correctamente',
                'data': json
            }, status = status.HTTP_200_OK) 
            
        except Exception as e:
            # Deshacemos la transaccion
            transaction.set_rollback(True)
            return Response({'errors': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Creamos la vista de ventas para obtener una factura
class GetInvoiceView(APIView):
    def get(self, request, tipo_de_comprobante: int, serie: str, numero: int):
        try:
            body = {
                    'operacion': 'consultar_comprobante',
                    'tipo_de_comprobante': tipo_de_comprobante,
                    'serie': serie,
                    'numero': numero
                }
            # Realizar la peticion
            nubeFactResponse = requests.post(
                url = environ.get('NUBEFACT_URL'),
                headers = {'Authorization': f'Bearer {environ.get("NUBEFACT_TOKEN")}'},
                json = body
            )
            
            # Obtener el json de la respuesta
            json = nubeFactResponse.json()
            
            # Verificar si la respuesta es correcta
            if nubeFactResponse.status_code != 200:
                raise Exception(json['errors'])
            
            # Retornar la respuesta            
            return Response({
                'message': 'Comprobante consultado correctamente',
                'data': json
            }, status = status.HTTP_200_OK)

        except Exception as e:
            return Response({'errors': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de ventas para crear un pago
class CreatePaymentView(APIView):
    def post(self, request):
        try:
            # Creamos el objeto mercadopago
            mp = mercadopago.SDK(environ.get('MERCADOPAGO_ACCESS_TOKEN'))
            
            # Creamos el objeto preference
            preference = {
                "items": [
                    {
                        "id": "123",
                        "title": "Zapatillas Adidas",
                        "quantity": 1,
                        "currency_id": "MXN",
                        "unit_price": 100
                    }
                ],
                'notification_url': 'http://de8f-2803-9810-61cc-b910-491e-ce45-db59-518c.ngrok-free.app/api/payment/notification'
            }
            
            # Creamos la preferencia
            preferenceResponse = mp.preference().create(preference)
            
            if preferenceResponse['status'] != 201:
                return Response({'errors': preferenceResponse['response']['message']}, status = status.HTTP_400_BAD_REQUEST)
            
            # Retornamos la respuesta
            return Response({
                'message': 'Pago generado correctamente',
                'data': preferenceResponse['response']
                }, status = status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'errors': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de ventas para notificar un pago    
class NotificationPaymentView(APIView):
    def post(self, request: Request):
        print(request.data)
        print(request.query_params)
        
        
        
        return Response({'message': 'Ok'}, status = status.HTTP_200_OK)

        