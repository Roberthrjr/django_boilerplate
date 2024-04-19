# Importamos la clase generics de DRF
from rest_framework import generics, status
# Importamos la clase Response de DRF
from rest_framework.response import Response
# Importamos el serializer
from .serializers import ProductSerializer, ProductModel, ProductUpdateSerializer, SaleSerializer, SaleModel
# Importamos la libreria cloudinary
from cloudinary.uploader import upload

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
            return Response({'message': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de productos para subir una imagen
class ProductUploadImageView(generics.GenericAPIView):
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
            imageName = uploadedImage['url'].split('/')[-1]
            # Obtenemos la ruta de la imagen
            imagePath = f'{uploadedImage["resource_type"]}/{uploadedImage["type"]}/v{uploadedImage["version"]}/{imageName}'
            # Retornamos la respuesta
            return Response({'url': imagePath})
        
        except Exception as e:
            # Retornamos la respuesta
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de ventas para obtener todas las ventas
class SaleView(generics.ListAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer    
    
# Creamos la vista de ventas para crear una venta
class SaleCreateView(generics.CreateAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer
    # Creamos el metodo create
    def create(self, request, *args, **kwargs):
        try:
            # Obtenemos los datos
            data = request.data
            # Verificamos si hay stock suficiente
            for item in data['detail']:
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
            # Creamos la venta
            return Response(data, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Creamos la vista de ventas para actualizar una venta
class SaleUpdateView(generics.UpdateAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer
    
# Creamos la vista de ventas para eliminar una venta
class SaleDeleteView(generics.DestroyAPIView):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer