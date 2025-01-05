 # 1. **Descripción**

Esta es la API del descontador automatico para infocol mapfre (electricistas), donde integra web scrapping dentro de auth/users/mapfre_scrapping para finalizar cada descuento. Dentro de apitosa encontraremos la API principal de uso del programa.
Dentro de auth/auth/ tienes la configuracion de channels que mas adelante en Configuracion veremos para editarlo a nuestro gusto.
 
 # 2. **Instalación**

 Importante si se usa con Djongo, instalar los requeriments y tener cuidado con las versiones por tema de compatibilidad.
 
 ```
pip install -r requeriments.txt
```
# 3. **Configuración**
Dentro de Auth/Auth/ hay varios archivos para configurar:
Para configurar la base de datos
Archivo auth/auth/settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'NAMEDB',
        'ENFORCE_SCHEMA': False,
        "CLIENT": {
            'host': 'mongodb://USSER:PASSWORD@IPDB:PORTDB/NAMEDB',
        }
    }
}

```

Seguridad:

Archivo auth/auth/mw.py
```
if not ip_address.startswith('192.168.'):
```
Esta linea revisa si la conexion procede de red interna local.

```
if not (country_code == 'ES') and ip_address not in ['54.38.180.107','45.135.180.216']:
```
Si no es local, revisa que la conexion sea Española y que sea de nuestros servidores, si no es asi error.
En caso de no querer usar esto anterior dentro de auth/auth/settings.py dentro de los MiddleWare:
```
MIDDLEWARE = [
    'auth.mw.RestrictIPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
Quitar la linea de "'auth.mw.RestrictIPMiddleware'," y listo.

Para configurar channels, dentro del archivo auth/routing.py tenemos la ruta o rutas disponibles para interactuar con channels. Veremos en nuestro caso, la ruta llama a info_partes que contiene:
Connect, Disconnect, Receive y send_progress. En caso de querer modificar el progreso de channels, modificar esta funcion de send_progress
```
    async def send_progress(self, event):
        # Envía actualizaciones de progreso al cliente
        await self.send(text_data=json.dumps(event['progress_data']))
```

En reincio.py tienes un script para mantener viva la API en caso de reinicio o similar, ejecutando este script en @reboot de crontab.
Modificar la linea y poner la ip de la maquina:
```
subprocess.Popen(["screen","-dmL","-Logfile", "/home/pi/logs/screenproyect.0","-S", "ezWater_api", "python3", "/home/ruta/manage.py/API", "runserver", "IPSERVER:PORT"])
```
