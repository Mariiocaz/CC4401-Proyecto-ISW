from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

    
# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(primary_key=True, blank=True, max_length=50)
    def __str__(self):
        return self.nombre  # name to be shown when called   

class User(AbstractUser): #clase para usuario
  saldo = models.FloatField(default=0) #variable saldo, contiene el saldo total para cada usuario
  categoria = models.ManyToManyField(Categoria)  # la llave foránea de categoria
 

class Transaccion(models.Model):  # Todolist able name that inherits models.Model
    titulo = models.CharField(max_length=200)  # un varchar de 200 caracteres
    monto = models.FloatField(default=0)  # un valor decimal
    fecha_creacion = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))  # una fecha en formato ISO yyyy-mm-dd, si esta vacia queda fecha actual
    categoria = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)  # la llave foránea de categoria
    duenno = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) #la llave foranea de usuario
    def __str__(self):
        return self.titulo  # name to be shown when called
      
      


