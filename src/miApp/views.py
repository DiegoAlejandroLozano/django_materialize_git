# coding=utf-8
from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django_materialize.settings import BASE_DIR
from django.urls import reverse
from miApp.models import Imagen
from django.contrib import messages
import os

# Create your views here.
def home( request ):
	"""
		Vista del home
	"""

	#Agregando la ruta y la url para la nueva locación
	locacion	= os.path.join( BASE_DIR, 'media/mis_fotos' )
	url 		= '/media/mis_fotos/'

	#Creando el FILESYSTEMSTORAGE
	fs = FileSystemStorage( location=locacion, base_url=url )	
		
	#Recuperando todas las imágenes almacenadas
	codigo_carousel = '<div class="carousel">'

	for imagen in Imagen.objects.all():

		codigo_carousel += """
			<a class="carousel-item" href="{url}">
				<img src="{url}">
			</a>
		""".format( url=fs.url( imagen.nombre ) )

	codigo_carousel += '</div>'


	return render( 
		request, 
		template_name = 'index.html', 
		context = {'codigo':codigo_carousel} 
	)


def agregar_imagen( request ):

	"""
		Vista utilizada para agregar una nueva imagen en la 
		base de datos y el sistema de almacenamiento de 
		Django
	"""

	#Si se ingresó por medio de una petición tipo POST
	if request.method == 'POST':

		#Leyendo la imagen de la petición
		archivo 			= request.FILES['imagen']

		#Agregando la ruta y la url para la nueva locación
		locacion	= os.path.join( BASE_DIR, 'media/mis_fotos' )
		url 		= '/media/mis_fotos/'

		#Creando el FILESYSTEMSTORAGE
		fs = FileSystemStorage( location=locacion, base_url=url )			

		#Guardando el archivo
		archivo_guardado	= fs.save( archivo.name, archivo )

		#Guardando el nombre en la base de datos
		imagen = Imagen( nombre = archivo_guardado )
		imagen.save()

		#Agregando un mensaje de confirmación
		messages.add_message( 
			request, 
			messages.SUCCESS, 
			'La imagen {} ha sido agregada'.format( archivo_guardado )
		)

	return HttpResponseRedirect( reverse( 'home' ) )


def tabla_imagenes( request ):

	"""
		Vista utilizada para mostrar una tabla con todas las imágenes almacenadas 
		en la base de datos y con la opción de eliminarlas.
	"""

	#leer todos los datos de la tabla
	imagenes = Imagen.objects.all()

	#creando el contexto
	contexto = {

		'imagenes'		:	imagenes

	}

	return render( request, template_name='tabla.html', context = contexto )

def eliminar_imagen( request, id_img ):

	"""
		Vista utilizada para realizar la operación
		de eliminar una imagen de la base de datos
	"""

	if request.method == 'POST':

		#Encontrar el objeto en la db
		imagen = Imagen.objects.get( id = id_img )

		#Creando el objeto FileSystemStorage
		locacion 	= os.path.join( BASE_DIR, 'media/mis_fotos' )
		url 		= '/media/mis_fotos/'

		fs = FileSystemStorage( location = locacion, base_url = url )

		#Borrando el archivo del sistema de almacenamiento de django
		fs.delete( imagen.nombre )

		#Borrando el registro de la base de datos
		imagen.delete()

		#Agregando un mensaje de confirmación
		messages.add_message(

			request,
			messages.SUCCESS,
			'La imagen {} ha sido eliminada'.format( imagen.nombre )

		)

	return HttpResponseRedirect( reverse( 'tabla' ) )