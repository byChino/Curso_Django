from django.contrib import admin
from django.urls import include, path
from Arcade.views import login, home, logout, register,config,Adventure,snake,perfil,delete_account,dinosaur_run,memory_game
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),  # Ruta principal que apunta al login
    path('home/', home, name='home'),  # Ruta para el home
    path('logout/', logout, name='logout'),  # Ruta para el logout
    path('register/', register, name='register'),  # Ruta para el registro
    path('perfil/ <int:id_user>/ ', perfil, name='perfil'),
    path('configuracion/ <int:id_user>/ ', config, name='config'),
    path('Adventure/', Adventure, name='Adventure'),
    path('snake/ <int:id_user>/ ', snake, name='snake'),
    path('delete-account/<int:id_user>/', delete_account, name='delete_account'),
     path('dinosaur-run/', dinosaur_run, name='dinosaur_run'),
     path('memory_game/', memory_game, name='memory_game'),
   # path('arcade/', include('arcade.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

