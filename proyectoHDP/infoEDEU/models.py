from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Estudiante(models.Model):
    id = models.AutoField(primary_key=True)
    universidad = models.CharField(max_length=45, verbose_name='Universidad', null=False)
    cantFisica = models.IntegerField(verbose_name='Cant. Fisica', null=False)
    cantIntelectual = models.IntegerField(verbose_name='Cant. Intelectual', null=False)
    cantSensorial = models.IntegerField(verbose_name='Cant. Sensorial', null=False)
    cantMental = models.IntegerField(verbose_name='Cant. Mental', null=False)
    cantMasculino = models.IntegerField(verbose_name='Cant. Masculino', null=False)
    cantFemenino = models.IntegerField(verbose_name='Cant. Femenino', null=False)
    cantTotal = models.IntegerField(verbose_name='Total', null=True)
  
    #Modifica la vista desde el usuario admin de python
    def __str__(self):
        fila = "Universidad " + self.universidad 
        return fila           
    
    #Elimina estudiantes desde el usuario admin de python
    def delete(self, using= None, keep_parents= False):
        super().delete()

    #Validaciones de Formularios
    def clean(self):
        super().clean()

        # Validar que no queden campos vacíos
        if (
            self.cantFisica is None or
            self.cantIntelectual is None or
            self.cantSensorial is None or
            self.cantMental is None or
            self.cantMasculino is None or
            self.cantFemenino is None
        ):
            raise ValidationError("Todos los campos son obligatorios.")

        # Validar que los campos numéricos sean mayores o iguales a cero
        if (
            self.cantFisica < 0 or
            self.cantIntelectual < 0 or
            self.cantSensorial < 0 or
            self.cantMental < 0 or
            self.cantMasculino < 0 or
            self.cantFemenino < 0
        ):
            raise ValidationError("Los campos de cantidad deben ser mayores o iguales a cero.")

        # Validar que la suma de cantFemenino y cantMasculino sea igual a la suma de los otros campos
        if self.cantFemenino + self.cantMasculino != self.cantFisica + self.cantIntelectual + self.cantSensorial + self.cantMental:
            raise ValidationError("La suma de Cant Femenino y Cant Masculino no coincide con la suma de los otros campos.")
        
        #Rellena automáticamente la cantidad total
        self.cantTotal = self.cantFemenino + self.cantMasculino