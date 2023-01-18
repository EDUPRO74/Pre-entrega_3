from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
from AppCoder.models import Curso, Profesor, Estudiante, Entregable
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from AppCoder.forms import CursoFormulario, profesorFormulario, estudianteFormulario, entregableFormulario




# Create your views here.

def inicio(request):

      return render(request, "AppCoder/inicio.html")

def cursos(request):

      if request.method == "POST":

            miFormulario = CursoFormulario(request.POST)
            print(miFormulario)

            if miFormulario.is_valid:
                  informacion = miFormulario.cleaned_data
                  curso = Curso(nombre=informacion["curso"], camada=informacion["camada"])
                  curso.save()
                  return render(request, "AppCoder/inicio.html")
      else:
            miFormulario = CursoFormulario()

      return render(request, "AppCoder/cursos.html", {"miFormulario": miFormulario})

def profesores(request):

      if request.method == 'POST':

            miFormulario = profesorFormulario(request.POST) 

            print(miFormulario)

            if miFormulario.is_valid:  

                  informacion = miFormulario.cleaned_data
                  profesor = Profesor (nombre=informacion['nombre'], apellido=informacion['apellido'],
                   email=informacion['email'], profesion=informacion['profesion']) 
                  profesor.save()

                  return render(request, "AppCoder/inicio.html") 

      else: 

            miFormulario= profesorFormulario() 

      return render(request, "AppCoder/profesores.html", {"miFormulario":miFormulario})


def estudiantes(request):

      if request.method == 'POST':

            miFormulario = estudianteFormulario(request.POST) 

            print(miFormulario)

            if miFormulario.is_valid:  

                  informacion = miFormulario.cleaned_data
                  estudiante = Estudiante (nombre=informacion['nombre'], apellido=informacion['apellido'],
                   email=informacion['email']) 
                  estudiante.save()

                  return render(request, "AppCoder/inicio.html")

      else: 

            miFormulario= estudianteFormulario() 

      return render(request, "AppCoder/estudiantes.html", {"miFormulario":miFormulario})
      


def entregables(request):

      if request.method == 'POST':

            miFormulario = entregableFormulario(request.POST) 

            print(miFormulario)

            if miFormulario.is_valid:   

                  informacion = miFormulario.cleaned_data
                  entregable = Entregable (nombre=informacion['nombre'], fechaDeEntrega=informacion['fecha'],
                   entregado=informacion['entregado']) 
                  entregable.save()

                  return render(request, "AppCoder/inicio.html")

      else: 

            miFormulario= entregableFormulario()

      return render(request, "AppCoder/entregables.html", {"miFormulario":miFormulario})


      
def buscar(request):

      if request.GET["camada"]:
            
            camada = request.GET['camada']
            cursos = Curso.objects.filter(camada__icontains=camada)
            
            return render(request, "AppCoder/inicio.html",{"cursos":cursos, "camada": camada})
      
      else: 
            respuesta = "No enviaste datos"
            
      return render(request,"AppCoder/inicio.html", {"respuesta":respuesta})



#funciones de extras de la calses:
def leerProfesores(request):

      profesores = Profesor.objects.all() #trae todos los profesores

      contexto= {"profesores":profesores} 

      return render(request, "AppCoder/leerProfesores.html",contexto)


def eliminarProfesor(request, profesor_nombre):

    profesor = Profesor.objects.get(nombre=profesor_nombre)
    profesor.delete()

    # vuelvo al menú
    profesores = Profesor.objects.all()  # trae todos los profesores

    contexto = {"profesores": profesores}

    return render(request, "AppCoder/leerProfesores.html", contexto)

def editarProfesor(request, profesor_nombre):

    # Recibe el nombre del profesor que vamos a modificar
    profesor = Profesor.objects.get(nombre=profesor_nombre)

    # Si es metodo POST hago lo mismo que el agregar
    if request.method == 'POST':

        # aquí mellega toda la información del html
        miFormulario = profesorFormulario(request.POST)

        print(miFormulario)

        if miFormulario.is_valid:  # Si pasó la validación de Django

            informacion = miFormulario.cleaned_data

            profesor.nombre = informacion['nombre']
            profesor.apellido = informacion['apellido']
            profesor.email = informacion['email']
            profesor.profesion = informacion['profesion']

            profesor.save()

            # Vuelvo al inicio o a donde quieran
            return render(request, "AppCoder/inicio.html")
    # En caso que no sea post
    else:
        # Creo el formulario con los datos que voy a modificar
        miFormulario = profesorFormulario(initial={'nombre': profesor.nombre, 'apellido': profesor.apellido,
                                                   'email': profesor.email, 'profesion': profesor.profesion})

    # Voy al html que me permite editar
    return render(request, "AppCoder/editarProfesor.html", {"miFormulario": miFormulario, "profesor_nombre": profesor_nombre})


class CursoList(ListView):

    model = Curso
    template_name = "AppCoder/cursos_list.html"
class CursoDetalle(DetailView):

    model = Curso
    template_name = "AppCoder/curso_detalle.html"

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

class CursoCreacion(CreateView):

    model = Curso
    success_url = "/AppCoder/curso/list"
    fields = ['nombre', 'camada']




class CursoUpdate(UpdateView):

    model = Curso
    success_url = "/AppCoder/curso/list"
    fields = ['nombre', 'camada']



class CursoDelete(DeleteView):

    model = Curso
    success_url = "/AppCoder/curso/list"


