import json
import os
from traceback import print_tb
from django.shortcuts import redirect, render
from base64 import b64decode, encode
from CoopresolWeb.settings import MEDIA_ROOT
from inicio.models import Contactos, Ideas,Proyectos,Equipo,Link,Correo,SociosJuridicos,categoria
from administracion.models import User
from django.http import HttpResponse, JsonResponse
from inicio.formulario import FormCorreo, FormProyectos,formEquipo, FormLINKS,FormCategoria,FormContactos, formPerJuridcica,creaciondeusuario
from inicio.formulario import FormUsuario
from inicio.views import Asociate
from .Serializers import SalaSerializer
from .jsontopdf import jsontoPDF,jsontoCSV
from django.core import serializers
from django.db.models import Q
import pyodbc
import pypyodbc
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout


from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

@login_required(login_url='autenticar')
def Administracion(request):

    pagina='administracion'
    CorreosPendiente =  Correo.objects.filter(Estado='Pendiente')
    query = request.GET.get('q') if request.GET.get('q') != None else ''

    contactos= Contactos.objects.filter(
        Q(Nombre__icontains=query) |
        Q(Apellido__icontains=query)|
        Q(solicitud__icontains=query)|
        Q(Cedula__icontains=query)
        ).order_by('-id')[:20]
    solicitudJuridica= SociosJuridicos.objects.filter(
        Q(NombreINS__icontains=query) |
        Q(WebSite=query)|
        Q(solicitud__icontains=query)|
        Q(RNC=query)
        ).order_by('-id')[:20]
    
    
    context={
        'contactos':contactos ,
        'solicitudJuridica':solicitudJuridica ,
        'pagina':pagina,
        'correosPendiente':CorreosPendiente
    }
    return render(request,'administracion/colectar.html',context)


@login_required(login_url='autenticar')
def ProyectosAdmin(request):
    
    proyectos = Proyectos.objects.all()
    pagina='administracion'
    formularioP = FormProyectos()
    CorreosPendiente =  Correo.objects.filter(Estado='Pendiente')
    ideas =  Ideas.objects.all()

    query = request.GET.get('q') if request.GET.get('q') != None else ''
    contactos= Contactos.objects.filter(
        Q(Nombre__icontains=query) |
        Q(Apellido__icontains=query)|
        Q(solicitud__icontains=query)
    
        )
    formulario =  FormProyectos(request.POST,request.FILES)       
  
#guardar el formulario a la base de  datos 
# 
    if formulario.is_valid():
        formulario.save()
        return redirect('administracion') 
    else:
        print(formulario.errors.as_data())
    
    context={
        'contactos':contactos ,
        'pagina':pagina,
        'formularioP':formularioP,
        'proyectos':proyectos,
        'correosPendiente':CorreosPendiente,
        'ideas':ideas
    }
    return render(request,'administracion/ProyectosA.html',context)



@login_required(login_url='autenticar')
def PaginaEquipo(request):
    
    pagina='administracion'
    equipo =  Equipo.objects.all()
    CorreosPendiente =  Correo.objects.filter(Estado='Pendiente')
    formulario = formEquipo()
    # query = request.GET.get('q') if request.GET.get('q') != None else ''
    # contactos= Contactos.objects.filter(
    #     Q(Nombre__icontains=query) |
    #     Q(Apellido__icontains=query)|
    #     Q(solicitud__icontains=query)
    
    #     )
    formulario =  formEquipo(request.POST,request.FILES)     
    if formulario.is_valid():
            formulario.save()
            return redirect('administracion') 
    
    context={
        'formulario':formulario,
        'pagina':pagina,
        'correosPendiente':CorreosPendiente,
        'equipo':equipo
    }
    return render(request,'administracion/Equipo.html',context)


@login_required(login_url='autenticar')
def EliminarPersona(request,pk):
            pagina='administracion'
            persona =  Equipo.objects.get(id=pk)        
            persona.delete()
            context ={
                'pagina':pagina,
            }
            return redirect('Equipo')


@login_required(login_url='autenticar')
def EliminarProyecto(request,pk):
            pagina='administracion'
            proyecto =  Proyectos.objects.get(id=pk)        
            proyecto.delete()
            context ={
                'pagina':pagina,
            }
            return redirect('ProyectosAdmin')


@login_required(login_url='autenticar')
def EliminarIdea(request,pk):
            pagina='administracion'
            Idea =  Ideas.objects.get(id=pk)        
            Idea.delete()
            context ={
                'pagina':pagina,
            }
            return redirect('ProyectosAdmin')


@login_required(login_url='autenticar')
def detalles(request,pk,model):

        if model =='idea':
            pagina='administracion'
            idea = Ideas.objects.get(id=pk)
            context ={
                'pagina':pagina,
                'idea':idea
            }
            return render(request,'administracion/vistaIdeas.html',context)
        CorreosPendiente =  Correo.objects.filter(Estado='Pendiente')
        proyectos = Proyectos.objects.get(id=pk)
        pagina='administracion'
        context = {
                'proyectos':proyectos,
                'correosPendiente':CorreosPendiente,
                'pagina':pagina
                
        }
        return render(request,'administracion/vistaProyecto.html',context)


@login_required(login_url='autenticar')
def Proyecto(request,pk):
        proyectos = Proyectos.objects.get(id=pk)
        pagina='administracion'
        context = {
                'proyectos':proyectos,
                'pagina':pagina
                
        }
        return render(request,'administracion/vistaProyecto.html',context)



@login_required(login_url='autenticar')      
def VideosPagina(request):
        formulario = FormLINKS()
        formuCategoria = FormCategoria()
        pagina='administracion'
        ideas =  Ideas.objects.all()
        CorreosPendiente =  Correo.objects.filter(Estado='Pendiente')
        link = Link.objects.all()
        categorias = categoria.objects.all()
        formulario =  FormLINKS(request.POST,request.FILES) 
        formuCategoria = FormCategoria(request.POST) 
        if formulario.is_valid():
            formulario.save()
            return redirect('administracion') 

        if formuCategoria.is_valid():
            formuCategoria.save()
            return redirect('administracion') 
        context = {
                'formulario':formulario,
                'formuCategoria':formuCategoria,
                'pagina':pagina,
                'correosPendiente':CorreosPendiente,
                'ideas':ideas,
                'categoria':categorias,
                'videos':link
        }   
        return render(request,'administracion/Videos.html',context)



@login_required(login_url='autenticar')
def eliminarSolicitudFisica(request,pk):
        pagina='administracion'
        solicitu =  Contactos.objects.get(id=pk)
        
        solicitu.delete()
                
        return redirect('administracion')



@login_required(login_url='autenticar')
def eliminarSolicitudJuridica(request,pk):
        pagina='administracion'
        solicitu =  SociosJuridicos.objects.get(id=pk)        
        solicitu.delete()
                
        return redirect('administracion')




@login_required(login_url='autenticar')
def eliminarVideos(request,pk):
        pagina='administracion'
        link =  Link.objects.get(id=pk)        
        link.delete()
                
        return redirect('administracion')


@login_required(login_url='autenticar')
def eliminarCategoria(request,pk):
        pagina='administracion'
        categorias =  categoria.objects.get(id=pk)        
        categorias.delete()
                
        return redirect('administracion')


@login_required(login_url='autenticar')
def Correos(request):
        pagina='administracion'
        CorreosData =  Correo.objects.all().order_by('-id')
        CorreosPendiente =  Correo.objects.filter(Estado='Pendiente').order_by('-id')

        context = {
            'pagina':pagina,
            'Correo':CorreosData,
            'correosPendiente':CorreosPendiente
                
        }
        return render(request,'administracion/Correos.html',context)


@login_required(login_url='autenticar')
def detalleCorreo(request,pk):
    
        CorreosPendiente =  Correo.objects.filter(Estado='Pendiente')
        formulario = FormCorreo()
        CorreosData = Correo.objects.get(id=pk)
        formulario = FormCorreo(instance=CorreosData)
        if CorreosData.Estado =='Pendiente':
            Correo.objects.filter(id=pk).update(Estado="Revisado")
        if request.method =='POST':
            CorreosData.delete()
            return redirect('Correos')

        # if formulario.is_valid():
        #         formulario.save()
        #         return redirect('Contactanos') 
        pagina='administracion'
        context = {
                'CorreosData':CorreosData,
                'pagina':pagina,
                'correosPendiente':CorreosPendiente,
                'formulario':formulario
        }
        return render(request,'administracion/vistaCorreo.html',context)



@login_required(login_url='autenticar')
def detalleSolicitudes(request,pk,model):
        
        if model =='Juridica':
            print(model)
            Solicitud = SociosJuridicos.objects.get(id=pk)
            formusol = formPerJuridcica(instance=Solicitud)
        if model =='persona':
            print(model)
            Solicitud = Contactos.objects.get(id=pk)
            formusol = FormContactos(instance=Solicitud)
            if request.method =='POST':
                Solicitud.Nombre= request.POST.get('Nombre')
                Solicitud.Apellido= request.POST.get('Apellido')
                Solicitud.Cedula= request.POST.get('Cedula')
                Solicitud.Direccion= request.POST.get('Direccion')
                Solicitud.email= request.POST.get('email')
                Solicitud.Telefono= request.POST.get('Telefono')
                Solicitud.Celular= request.POST.get('Celular')
                Solicitud.Patrocinador= request.POST.get('Patrocinador')
                Solicitud.LugarNacimiento= request.POST.get('LugarNacimiento')
                Solicitud.FechaNacimiento= request.POST.get('FechaNacimiento')
                Solicitud.Hijos= request.POST.get('Hijos')
                Solicitud.hijas= request.POST.get('hijas')
                Solicitud.EstadoCivil= request.POST.get('EstadoCivil')
                Solicitud.LugarTrabajo= request.POST.get('LugarTrabajo')
                Solicitud.TelTrabajo= request.POST.get('TelTrabajo')
                Solicitud.DireccionTrabajo= request.POST.get('DireccionTrabajo')
                Solicitud.Estado= request.POST.get('Estado')
                Solicitud.save()
                return redirect('administracion')

        # if formulario.is_valid():
        #         formulario.save()
        #         return redirect('Contactanos') 
        pagina='administracion'
        context = {
                # 'Solicitud':Solicitud,
                'pagina':pagina,
                'formusol':formusol

        }
        return render(request,'administracion/vistaSolicitudes.html',context)



@login_required(login_url='autenticar')
def ideas(request):
        pagina='administracion'
        ideas =  Ideas.objects.all()
        

        context = {
            'pagina':pagina,
          
            
            
                
        }
        return render(request,'administracion/ideas.html',context)


@login_required(login_url='autenticar')
def Repotes(request):
        pagina='administracion'
        SolicitudesF =  Contactos.objects.all()
        SolicitudesJ =  SociosJuridicos.objects.all()


        context = {
            'pagina':pagina,
            'SolicitudesF':SolicitudesF,
            'SolicitudesJ':SolicitudesJ,
            
                
        }
        return render(request,'administracion/Reporte.html',context)


def autenticacion(request):

    pagina ='administracion'
    if request.user.is_authenticated:
        return redirect('administracion')
    

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        contra = request.POST.get('contra')
        try:
            usuario = User.objects.get(username=username)
        except:
            messages.error(request, 'Usuario No Existe')
        
        usuario = authenticate(request,username=username,password=contra)
        
        if usuario is not None:
            login(request,usuario)
            return redirect('administracion')
        else:
            messages.error(request, 'Usuario o contrasenia No Existe')
    context={'pagina':pagina}
    return render(request,'administracion/autenticar.html',context)
    


def cerrarSesion(request):
    logout(request)
    return redirect('autenticar')

def registrarUsuario(request):
    #pagina = 'registrar'

    formulario = creaciondeusuario()
    if request.method == 'POST':
        formulario = creaciondeusuario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.username = usuario.username.lower()
            usuario.save()
            login(request, usuario)
            return redirect('inicio')
        else:
            messages.error(request,'revisa bien los datos please')
    context = {'formulario':formulario}
    return render(request,'incio/autenticacion.html',context)

def eliminarUsuario(request,pk):
    usuario = User.objects.get(id=pk)
    usuario.delete()
    return redirect('usuarios')


def editarUsuario(request):
    
    email = request.POST.get('email')
    if request.method == "POST":
        correo = User.objects.get(email=email)
        formulario = FormUsuario(request.POST ,instance=correo)
        if formulario.is_valid():
            usuario = formulario.save()
            usuario.set_password(request.POST.get('password'))
            usuario.save()
            
        else:
            print('error')
    return redirect('administracion')
    
def crearUsuario(request):
    #pagina = 'registrar'

    formulario = creaciondeusuario()
    if request.method == 'POST':
        formulario = creaciondeusuario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.username = usuario.username.lower()
            usuario.save()
            return redirect('administracion')
        else:
            print('provlemas')
    context = {'formulario':formulario}
    return redirect('usuarios')

def usuarios(request):
    pagina= "administracion"
    usuarios = User.objects.all()
    formulario = FormUsuario()
    formularioCcreacion = creaciondeusuario()


    context = {
        'usuarios':usuarios,
        'pagina':pagina,
        'formulario':formulario,
        'formularioCcreacion':formularioCcreacion
    }
    return render(request,'administracion/usuarios.html',context)
