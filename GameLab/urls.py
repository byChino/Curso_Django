from django.contrib import admin
from django.urls import include, path
from Arcade.views import login, home, logout, register,config,Adventure,snake
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),  # Ruta principal que apunta al login
    path('home/', home, name='home'),  # Ruta para el home
    path('logout/', logout, name='logout'),  # Ruta para el logout
    path('register/', register, name='register'),  # Ruta para el registro

    path('configuracion/ <int:id_user>/ ', config, name='config'),
    path('Adventure/', Adventure, name='Adventure'),
    path('snake/ <int:id_user>/ ', snake, name='snake'),
   # path('arcade/', include('arcade.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

