# Curso Django



## Requisitos

Asegúrate de tener instalado lo siguiente antes de comenzar:

- Python 3.x
- pip (administrador de paquetes de Python)
- PostgreSQL (o el sistema de bases de datos que estés utilizando)

## Pasos para configurar el proyecto

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### 1. Clonar el repositorio

Primero, clona el repositorio desde GitHub:

```bash
git clone https://github.com/byChino/RubricaUX.git
cd RubricaUX
```
### 2. Crear el entorno virtual
```bash
python -m venv venv
venv/scripts/activate
```
### 3. Instalar las dependencias
```bash
pip install -r requeriments.txt
```
☝🏿Si falla instalarlos manualmente

### 4. Configurar la base de datos
``` bash
DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.postgresql',
        
        'NAME': 'nombre_base_datos',
        
        'USER': 'tu_usuario',
        
        'PASSWORD': 'tu_contraseña',
        
        'HOST': 'localhost',
        
        'PORT': '5432',
        
    }
    
}
```

### 5. Aplicar las migraciones
Aplica las migraciones para crear las tablas en la base de datos:
```bash
python manage.py migrate
```

Nota: Borrar el contenido de la carpeta migratas antes de usar este comando, y debes aplicar el siguiente comando
```bash
python manage.py makemigrations
```
Tambien si quieres cargar un modelo en particular solo pon el nombre adelante de makemigrations

### 6. Crear un superusuario
Crea un superusuario para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```
Sigue las instrucciones en pantalla para crear el superusuario.

Usuario: SU

Corre: Tu correo electronico

Contrasenia:SU1234


### 7. Ejecutar el servidor de desarrollo
Finalmente, ejecuta el servidor de desarrollo de Django:
```bash
python manage.py runserver
```
