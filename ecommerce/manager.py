# Importamos la clase BaseUserManager de Django
from django.contrib.auth.models import BaseUserManager

# Se define una clase que hereda de BaseUserManager
class UserManager(BaseUserManager):
    # Creamos un metodo para crear un usuario
    def create_user(self, email, password=None):
        # Verificamos si se proporciono un email
        if not email:
            # Generamos una excepcion si no se proporciono un email
            raise ValueError('Los usuarios deben tener una dirección de correo electrónico')

        # Creamos un nuevo usuario con el email normalizado
        user = self.model(
            email = self.normalize_email(email),
        )
        # Establecemos la contraseña del usuario
        user.set_password(password)
        # Guardamos el usuario en la base de datos
        user.save(using=self._db)
        # Retornamos el usuario
        return user
    
    # Creamos un metodo para crear un usuario administrador
    def create_superuser(self, email, password=None):
        # Creamos un nuevo usuario con el email normalizado
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
        )
        # Establecemos que el usuario es administrador
        user.is_admin = True
        # Guardamos el usuario en la base de datos
        user.save(using=self._db)
        # Retornamos el usuario
        return user