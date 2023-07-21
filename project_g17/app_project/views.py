#####View del Usuario#####

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from app_project.models import Transaccion, Categoria
from django.http import HttpResponseRedirect
from django.http import response
from app_project.models import User
from django.http import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from .validations import *

 

# Create your views here.

def index(request):
    return render(request, "app_project/index.html") #Mostrar el template

####Register View#####
def register_user(request):
    if request.method == 'GET': #Si estamos cargando la página
      return render(request, "app_project/register_user.html") #Mostrar el template

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
      
      #Tomar los elementos del formulario que vienen en request.POST
      nombre = request.POST['nombre']
      contraseña = request.POST['contrasenna']
      #apodo = request.POST['apodo']
      es_valido, mensaje_error = validate_register(nombre, contraseña)
      if es_valido:
        try:
          #Crear el nuevo usuario
          User.objects.create_user(username=nombre, password=contraseña)

          #Redireccionar la página /info (cambiar según nombre de la página)
          return redirect("user-account")
        except:
          return render(request, "app_project/register_user.html", {"error" : "* El usuario ya existe."})
      else:
        return render(request, "app_project/register_user.html", {"error" : mensaje_error})
    
####View de la App#####

def login_user(request): # login de la app
    
    mensaje_error = "* Usuario o contraseña incorrectos, por favor intente de nuevo."
    if request.user.is_authenticated:
        return redirect("user-account")
    if request.method == 'GET': # si estamos cargando la página
        return render(request, "app_project/login.html")    # mostrar template
    if request.method == 'POST':
        username = request.POST['username']
        contrasenna = request.POST['contrasenna']
        usuario = authenticate(username=username,password=contrasenna)

        if usuario is not None:
            login(request,usuario)
            return redirect("user-account")
        else:
            return render(request, "app_project/login.html" ,{"error": mensaje_error})  # se redirecciona con error de login
        
        
def logout_user(request):
   logout(request)
   return redirect("/")
   
def list_transacciones(request):
  if request.user.is_authenticated:
    categorias = request.user.categoria.all().values() # Mando las categorias para usarlas en el modal del modify
    transacciones = Transaccion.objects.filter(duenno=request.user).values()
    if request.method == 'GET':
        #obtener rango de fechas + categoria
        fecha_inicio_str = request.GET.get('fecha-inicio', '')
        fecha_fin_str = request.GET.get('fecha-fin', '')
        categoria_id = request.GET.get('categoria-filtro', '')

        #si existen las tres variables
        if fecha_inicio_str and fecha_fin_str and categoria_id:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            evento = transacciones.filter(fecha_creacion__range=(fecha_inicio, fecha_fin))
            transacciones = evento.filter(categoria=categoria_id)
           
        #si solo existen fechas   
        elif fecha_inicio_str and fecha_fin_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            transacciones = transacciones.filter(fecha_creacion__range=(fecha_inicio, fecha_fin))

        #si solo existe categoria
        elif categoria_id:
          transacciones = transacciones.filter(categoria=categoria_id)
        
    data = {'transacciones': list(transacciones), 'categorias': list(categorias)}
    return JsonResponse(data)
  else:
    return redirect("login")


def delete_transaccion(request):
  if request.user.is_authenticated:
    id = request.GET.get('id', '')
    del_transaccion = get_object_or_404(Transaccion, pk=id, duenno=request.user)
    monto = del_transaccion.monto
    request.user.saldo -= float(monto)
    request.user.save()
    del_transaccion.delete()
    data = {'saldoFinal' : request.user.saldo }
    return JsonResponse(data)
  else:
    return redirect("login")
      
 
 
errores = [
   "Error de categoría: Por favor ingrese una categoría válida.",
   "Error al agregar transacción: Por favor ingrese parámetros de transacción válidos (nombre y categoría no vacíos, monto numérico).",
   "Por favor ingrese parámetros de transacción válidos al modificar (nombre y categoría no vacíos, monto numérico)."
]

def modify_transaccion(request):
  if request.user.is_authenticated and request.method == 'POST':
    id = request.POST["idMod"]
    tituloMod = request.POST["nameMod"]  # titulo de la transaccion
    montoMod = request.POST["amountMod"]  # monto de la transaccion
    fecha_creacionMod = request.POST["dateMod"] #fecha de la transaccion
    nombre_categoriaMod = request.POST["classMod"]  # nombre de la categoria
    categoriaMod = get_object_or_404(Categoria, nombre=nombre_categoriaMod)
    busqueda = get_object_or_404(Transaccion, pk=id, duenno=request.user)

    try:  # se intenta hacer la modificación
      if (tituloMod == "" or nombre_categoriaMod == ""):  # si son vacíos
        raise Exception
      busqueda.titulo = tituloMod
      montoIncial = busqueda.monto
      busqueda.monto = montoMod
      busqueda.fecha_creacion = fecha_creacionMod
      busqueda.categoria = categoriaMod
      request.user.saldo += (float(montoMod) - float(montoIncial)) # se actualiza el saldo
      request.user.save()
      busqueda.save()  # guardar la busqueda en la base de datos.
      data = {'saldo': request.user.saldo, 'error':""}
    except: # si falla
      data = {'saldo': request.user.saldo, 'error':errores[2]}
      return JsonResponse(data)

    return JsonResponse(data)

  else:
    return redirect("login")
  
def transacciones(request, error_id=None): # página principal
    if request.method == "GET":
      if request.user.is_authenticated:
        
        categorias = request.user.categoria.all()  # getting all categories with object manager
        transacciones = Transaccion.objects.filter(duenno=request.user)# quering all todos with the object manager
        if(error_id == "e_categoria"):
          return render(request, "app_project/user-account.html", {"transacciones": transacciones, "categorias": categorias, "error_categoria":errores[0]})
        elif(error_id == "e_transaccion"):
          return render(request, "app_project/user-account.html", {"transacciones": transacciones, "categorias": categorias, "error_transaccion":errores[1]}) 
                        
        return render(request, "app_project/user-account.html", {"transacciones": transacciones, "categorias": categorias})
      else:
        return redirect("login")

    elif request.method == "POST":  # revisar si el método de la request es POST
      if request.user.is_authenticated:
        if "taskCategory" in request.POST:
          nombre_categoria = request.POST["categoryAdd"]
          if(nombre_categoria == ''): # si el nombre es vacio
            return redirect('http://127.0.0.1:8000/user_account/e_categoria') # se retorna con el error
             
          # si no es vacío, se continúa
          categoria = Categoria.objects.filter(nombre=nombre_categoria).first()
          if categoria is None:
            try:  # si algo sale mal
              categoria = Categoria(nombre=nombre_categoria)
            except:
              return redirect('http://127.0.0.1:8000/user_account/e_categoria') # se retorna con el error  
            
            categoria.save()
            request.user.categoria.add(categoria)
          else:
            request.user.categoria.add(categoria)
        
        elif "taskDelCategory" in request.POST:
          nombre_categoria = request.POST["categoryDel"]
          if(nombre_categoria == ''): # si el nombre es vacio
            return redirect('http://127.0.0.1:8000/user_account/e_categoria') # se retorna con el error
          
          # si no es vacío, se continúa
          categoria = Categoria.objects.filter(nombre=nombre_categoria).first()
          if categoria is None:
            try:  # si algo sale mal
              categoria = Categoria(nombre=nombre_categoria)
            except:
              return redirect('http://127.0.0.1:8000/user_account/e_categoria') # se retorna con el error
            # Categoría placeholder para las transacciones que tuvieron esa categoría que se borrará
            s_cat, created = Categoria.objects.get_or_create(nombre="Sin categoría")
            # Se actualiza la categoría
            transacciones = Transaccion.objects.filter(duenno=request.user, categoria=categoria).update(categoria=s_cat)
            # Se borra la categoría del usuario
            request.user.categoria.remove(categoria)
          else:
            # Categoría placeholder para las transacciones que tuvieron esa categoría que se borrará
            s_cat, created = Categoria.objects.get_or_create(nombre="Sin categoría")
            # Se actualiza la categoría
            transacciones = Transaccion.objects.filter(duenno=request.user, categoria=categoria).update(categoria=s_cat)
            # Se borra la categoría del usuario
            request.user.categoria.remove(categoria)
            # Se busca si algún usuario tiene esa categoría
            categoria_exists = User.objects.filter(categoria__nombre=categoria.nombre).exists()
            # Si ningún usuario tiene una categoría, también se borra
            if not categoria_exists:
              categoria.delete()
            

           
          
        elif "taskAdd" in request.POST:  # verificar si la request es para agregar una tarea (esto está definido en el button)
            titulo = request.POST["nameAdd"]  # titulo de la transaccion
            monto = request.POST["amountAdd"]  # monto de la transaccion
            fecha_creacion = request.POST["dateAdd"] #fecha de la transaccion
            nombre_categoria = request.POST["classAdd"]  # nombre de la categoria
            categoria = get_object_or_404(Categoria, nombre=nombre_categoria)

            if(titulo == "" or nombre_categoria == ""): # si son vacíos
              return redirect('http://127.0.0.1:8000/user_account/e_transaccion') # se retorna con el error

            try:  # se intenta modifcar el monto
              request.user.saldo += float(monto)
              request.user.save()
            except: # si falla retornar error
              return redirect('http://127.0.0.1:8000/user_account/e_transaccion') # se retorna con el error
            
            if fecha_creacion != "":
                try:
                  nueva_transaccion = Transaccion(titulo=titulo, monto=monto, fecha_creacion=fecha_creacion, categoria=categoria, duenno=request.user) # Crear la transaccion
                  nueva_transaccion.save()
                except:
                  return redirect('http://127.0.0.1:8000/e_transaccion') # se retorna con el error 

            else:
                try:
                  nueva_transaccion = Transaccion.objects.create(titulo=titulo, monto=monto, categoria=categoria, duenno=request.user)  # Crear la transaccion  # guardar la transaccion en la base de datos.   
                except:
                  return redirect('http://127.0.0.1:8000/e_transaccion') # se retorna con el error
          
        return redirect("user-account")
      
      else:
        return redirect("login") # recargar la página.
