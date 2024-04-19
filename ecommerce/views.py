# Importamos la clase generics de DRF
from rest_framework import generics
# Importamos la clase Response de DRF
from rest_framework.response import Response
# Importamos el serializer
from .serializers import ProductSerializer, ProductModel, ProductUpdateSerializer
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

class ProductUpdateView(generics.UpdateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductUpdateSerializer

class ProductDeleteView(generics.DestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

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
                raise Response({'message': 'No se ha facilitado ninguna imagen'}, status=400)
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
            return Response({'message': str(e)}, status=400)