from django.shortcuts import render, redirect
from django.http import HttpResponse
from infoEDEU.decorators import userIsAdmin
from infoEDEU.models import Estudiante
from infoEDEU.forms import EstudianteForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import plotly.graph_objects as go
from django.contrib import messages

# Create your views here.

def inicio(request):
    # Obtener los datos de la base de datos
    estudiantes = Estudiante.objects.all()
    universidades = [estudiante.universidad for estudiante in estudiantes]
    fisica = [estudiante.cantFisica for estudiante in estudiantes]    
    intelectual = [estudiante.cantIntelectual for estudiante in estudiantes]    
    sensorial = [estudiante.cantSensorial for estudiante in estudiantes]    
    mental = [estudiante.cantMental for estudiante in estudiantes]    
    femenino = [estudiante.cantFemenino for estudiante in estudiantes]    
    masculino = [estudiante.cantMasculino for estudiante in estudiantes]
    total = [estudiante.cantTotal for estudiante in estudiantes]

    # Crear los gráficos
    graficoPastel = go.Figure(data=[go.Pie(labels=universidades, values=total)])
    graficoLineaFemMas = go.Figure()
    graficoLineaDisc = go.Figure()

    #------gráfico pastel
    graficoPastel.update_layout(
        width=600, 
        height=600, 
        title="Universidad - Cantidad total de EDSU")
    
    graficoPastel.update_traces(textinfo='value')

    #-------grafico barras soble fem-mas
    # Añadir barras para la cantidad femenina
    graficoLineaFemMas.add_trace(go.Bar(
        x=universidades,
        y=femenino,
        name='Femenino'
    ))

    # Añadir barras para la cantidad masculina
    graficoLineaFemMas.add_trace(go.Bar(
        x=universidades,
        y=masculino,
        name='Masculino'
    ))

    graficoLineaFemMas.update_layout(
        width=600, 
        height=500, 
        title="Cantidad de Estudiantes por Género",
        xaxis_title="Universidades",
        yaxis_title="Genero")

    #-------grafico barras cuadruple tipoDiscapacidad
    # Añadir barras para la discapacidad fisica
    graficoLineaDisc.add_trace(go.Bar(
        x=universidades,
        y=fisica,
        name='Fisica'
    ))

    # Añadir barras para la discapacidad intelectual
    graficoLineaDisc.add_trace(go.Bar(
        x=universidades,
        y=intelectual,
        name='Intelectual'
    ))

    # Añadir barras para la discapacidad sensorial
    graficoLineaDisc.add_trace(go.Bar(
        x=universidades,
        y=sensorial,
        name='Sensorial'
    ))

    # Añadir barras para la discapacidad mental
    graficoLineaDisc.add_trace(go.Bar(
        x=universidades,
        y=mental,
        name='Mental'
    ))

    graficoLineaDisc.update_layout(
         width=600, 
        height=500, 
    title="Cantidad de Estudiantes por Discapacidad",
    xaxis_title="Universidades",
    yaxis_title="Tipo de Discapacidad")

    # Convierte los gráficos a HTML
    graph_1 = graficoPastel.to_html(full_html=False)
    graph_2 = graficoLineaFemMas.to_html(full_html=False)
    graph_3 = graficoLineaDisc.to_html(full_html=False)

    # Renderizar la plantilla con los datos de los estudiantes y el gráfico
    return render(request, 'estudiantes/index.html', 
                  {'estudiantes': estudiantes, 
                   'graph_1': graph_1,
                   'graph_2': graph_2,
                   'graph_3': graph_3,
                })

#Para el CRUD
@userIsAdmin
def crear(request):
    if request.method == 'POST':
        formulario=EstudianteForm(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Información agregada correctamente") #notificación 
            return redirect('inicio')    
    else:
        formulario = EstudianteForm()
    return render(request, 'estudiantes/crear.html', {'formulario':formulario}) 

@userIsAdmin
def editar(request, id):
    estudiante=Estudiante.objects.get(id=id)
    formulario=EstudianteForm(request.POST or None, request.FILES or None, instance=estudiante)
    if formulario.is_valid() and request.POST:
        formulario.save() 
        m1=messages.success(request, "Información editada correctamente") #notificación 
        return redirect('inicio')    
    return render(request, 'estudiantes/editar.html',{'formulario':formulario}) 

@userIsAdmin
def eliminar(request, id):
    estudiante=Estudiante.objects.get(id=id)
    estudiante.delete()
    m1=messages.success(request, "Información eliminada correctamente") #notificación 
    return redirect('inicio')    


#Para el inicio de sesión
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html')

#no se usa, ya que no hay forma de registrar usuarios
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('inicio')
        else:
            return HttpResponse ("Usuario o contraseña es incorrecta!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('inicio')

#no se usan, pero para futuros cambios
#def inicio(request):
    estudiantes=Estudiante.objects.all()
    return render(request, 'estudiantes/index.html', {'estudiantes':estudiantes}) 
 
#def estudiantes(request):
    estudiantes=Estudiante.objects.all()
    return render(request, 'estudiantes/index.html', {'estudiantes':estudiantes}) 

