from django.db import models

# Create your models here.

class Imagen( models.Model ):

	"""
		Modelo utilizado para guardar el nombre de las imágenes subidas por el usuario
	"""

	nombre = models.CharField( max_length=100 )

	def __str__(self):
		return self.nombre

	class Meta:
		db_table 				= 'imagenes'
		verbose_name 			= 'imagen'
		verbose_name_plural 	= 'imagenes'