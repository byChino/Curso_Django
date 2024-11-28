import json
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from  .forms import PersonaForm, UserForm
from .models import JuegoSnake, Persona
from django.contrib.auth import update_session_auth_hash  # Para mantener la sesión activa tras cambiar la contraseña
from django.views.decorators.csrf import csrf_exempt
# Vista para el login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # Autenticación con Django
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Iniciar sesión
            auth_login(request, user)
            return redirect('home')  # Redirigir al home
        else:
            # Si las credenciales son inválidas, muestra un mensaje de error
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'login.html')  # Renderiza la plantilla de login


# Vista para el home (requiere autenticación)
from django.db.models import Max
def home(request):
    # Obtener el ranking con los datos requeridos
    ranking = (
        JuegoSnake.objects.values("user__username")
        .annotate(
            max_puntaje=Max("puntaje"),
            max_nivel=Max("nivelMax"),
            max_tiempo=Max("tiempoMax"),
        )
        .order_by("-max_puntaje")
    )

    context = {"ranking": ranking}
    return render(request, "home.html", context) # Renderiza la plantilla del home


# Vista para el logout
def logout(request):
    auth_logout(request)  # Cerrar sesión
    return redirect('login')  # Redirige al login

def register(request):
    form=   UserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # Validación de contraseñas
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})
        # Crear usuario
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            return redirect('login')
        except Exception as e:
            return render(request, 'register.html', {'error': str(e)})
    return render(request, 'register.html', {'form': form})



@login_required
def config(request, id_user):
    # Obtiene el usuario actual
    user = get_object_or_404(User, id=id_user)

    # Obtiene o crea una instancia vacía de Persona asociada al usuario
    persona, created = Persona.objects.get_or_create(user=user)

    # Formularios inicializados con instancias
    formPersona = PersonaForm(instance=persona)

    if request.method == 'POST':
        if 'nombre' in request.POST:  # Formulario de datos personales
            formPersona = PersonaForm(request.POST, request.FILES, instance=persona)
            if formPersona.is_valid():
                formPersona.save()
                messages.success(request, "¡Datos personales guardados correctamente!")
                return redirect('config', id_user=id_user)
            else:
                messages.error(request, "Por favor corrige los errores en el formulario de datos personales.")

        elif 'username' in request.POST:  # Formulario de usuario
            username = request.POST.get('username', '').strip()
            password_actual = request.POST.get('password-actual', '')
            password_new = request.POST.get('password-new', '')
            password_confirm = request.POST.get('password-confirm', '')

            # Validar contraseña actual
            if not user.check_password(password_actual):
                messages.error(request, "La contraseña actual no es correcta.")
            elif password_new != password_confirm:
                messages.error(request, "La nueva contraseña no coincide con la confirmación.")
            else:
                # Actualizar usuario
                if username:
                    user.username = username
                if password_new:
                    user.set_password(password_new)
                user.save()
                update_session_auth_hash(request, user)  # Mantiene la sesión activa tras cambiar la contraseña
                messages.success(request, "¡Datos de usuario guardados correctamente!")
                return redirect('config', id_user=id_user)

    return render(request, 'configuracion.html', {'user': user, 'persona': persona, 'formPersona': formPersona})


  



def Adventure(request):
    return render(request, 'games/Adventure.html')
  
@csrf_exempt  # Solo para pruebas locales; elimina esta línea en producción
@login_required
def snake(request, id_user):
    user = get_object_or_404(User, id=id_user)

    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Leer el cuerpo JSON
            puntaje = data.get("puntaje", 0)
            tiempo = data.get("tiempo", 0)
            nivel = data.get("nivel", 0)

            # Crear un nuevo registro de juego para el usuario
            JuegoSnake.objects.create(
                user=user,
                puntaje=puntaje,
                tiempoMax=tiempo,
                nivelMax=nivel
            )

            return JsonResponse({"success": True, "message": "Partida registrada correctamente."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return render(request, 'games/snake.html')

@login_required
def perfil(request, id_user):
    user = get_object_or_404(User, id=id_user)
    persona = get_object_or_404(Persona, user=user)
    sknake = JuegoSnake.objects.filter(user=user).order_by('-puntaje')
    return render(request, 'perfil.html', {'user': user, 'persona':persona ,'sknake':sknake}) 



@login_required
def delete_account(request, id_user):
    user = get_object_or_404(User, id=id_user)
    
    if request.method == "POST":
        # Elimina la cuenta
        user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada con éxito.")
        
        # Cierra la sesión
        logout(request)
        
        # Redirige al login
        return redirect('login')

    return redirect('config', id_user=id_user)

def dinosaur_run(request):
    return render(request, 'games/Dino_Runner.html')



def memory_game(request):
    return render(request, 'games/memory_game.html')