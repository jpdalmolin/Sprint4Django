from django.http import HttpResponse
from django.shortcuts import render
from AppCoder.models import Animales,Avatar
from django.template import Template,Context,loader
from AppCoder.forms import BlogFormulario
from AppCoder.forms import UserEditForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django import forms
from AppCoder.forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views import generic

@login_required
def animales(request):

      return render(request, "AppCoder/animales.html")



def busquedaNombre(request):

      return render(request, "AppCoder/busquedaNombre.html")


def resultadosBusqueda(request):

      if request.GET['nombre']:
      #respuesta= f" ESTOY BUSCANDO AL FAMILIAR DE NOMBRE : {request.GET['nombre']}"
            nombre= request.GET['nombre']
            animal=Animales.objects.filter(nombre__icontains=nombre) 

            return render(request, "AppCoder/resultadosBusqueda.html",{"animal":animal,"nombre":nombre})

      else:
            respuesta= "No enviaste datos"

      return HttpResponse(respuesta)


class AnimalesList(LoginRequiredMixin,ListView):

      model=Animales
      template_name ="AppCoder/animales_list.html"

class AnimalesDetalle(generic.DetailView):

      model=Animales
      template_name="AppCoder/animales_detalle.html"

class AnimalesCreacion(CreateView):

      model=Animales
      success_url="/AppCoder/animales/list"
      fields=['nombre','tipo','fechaDeNacimiento']

class AnimalesUpdate(UpdateView):

      model=Animales
      success_url="/AppCoder/animales/list"
      fields=['nombre','tipo','fechaDeNacimiento']

class AnimalesDelete(DeleteView):

      model=Animales
      success_url="/AppCoder/animales/list"
      
def login_request(request):

      if request.method =="POST":
            form = AuthenticationForm(request,data=request.POST)
            print(form)
            if form.is_valid():
                  usuario=form.cleaned_data.get('username')
                  contra=form.cleaned_data.get('password')
                  print(usuario,contra)
                  user= authenticate(username=usuario, password=contra)
                  print(user)
                  if user is not None:
                        login(request,user)

                        return render(request,"AppCoder/inicio.html", {"mensaje":f"Bienvenido {usuario}"})
                  else:
                        print(2)
                        return render(request,"AppCoder/inicio.html", {"mensaje":"Error datos incorrectos"})

            else:

                  return render(request,"AppCoder/inicio.html", {"mensaje":"Error, formulario erroneo"})
      form=AuthenticationForm()
      print(3)
      return render(request,"AppCoder/login.html", {'form':form})

def register(request):

      if request.method == 'POST':

            form= UserCreationForm(request.POST)

            if form.is_valid():

                  username=form.cleaned_data['username']
                  form.save()
                  return render(request,"AppCoder/inicio.html", {"mensaje":"Usuario Creado !"})

      else:
            form=UserRegisterForm()

      return render(request,"AppCoder/registro.html",{"form":form})      

@login_required
def editarPerfil(request):
      #Instancia del login
      usuario =request.user
      
      if request.method =='POST':
            miFormulario=UserEditForm(request.POST)
            if miFormulario.is_valid():

                  informacion=miFormulario.cleaned_data
                  #datos que se modificaran
                  usuario.email=informacion['email']
                  usuario.password1=informacion['password1']
                  usuario.password2=informacion['password1']
                  usuario.save()

                  return render(request, "AppCoder/inicio.html") #vuelve al inicio
            
      else:

            miFormulario=UserEditForm(initial={'email':usuario.email})

      return render(request, "AppCoder/editarPerfil.html",{"miFormulario":miFormulario, "usuario":usuario})


def inicio(request):

      avatares = Avatar.objects.filter(user=request.user.id)

      try:
            return render(request, "AppCoder/inicio.html", {"url":avatares[0].imagen.url} )
      except IndexError:
            return render(request, "AppCoder/inicio.html")


def blogFormulario(request):
      
      if request.method == 'POST':

            miFormulario= BlogFormulario(request.POST,request.FILES)
            print(miFormulario)
            
            if miFormulario.is_valid:

                  informacion =miFormulario.cleaned_data
                  print(informacion)
                  
                  posts=Post(title=informacion['title'], content=informacion['content'],image=informacion['image'],author=informacion['author'])

                  posts.save()

                  return render(request, "AppCoder/inicio.html")

      else:

            miFormulario= BlogFormulario()

      return render(request, "AppCoder/blogFormulario.html", {"miFormulario":miFormulario})


def blog(request):
    posts = Post.objects.all()
    return render(request, "AppCoder/blog.html", {'posts':posts})

class BlogList(ListView):

      model=Post
      template_name= "AppCoder/post_list.html"

class BlogDetalle(DetailView):

      model=Post
      template_name ="AppCoder/post_detalle.html"

    