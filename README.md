# Sistema de Ingreso y Asistencia Mediante Sensores 📡

Este proyecto es una aplicación web que permite el registro de asistencia de los estudiantes de la Fundacion Universitaria de popayan, mediante el uso de un sensor RFID y una Raspberry Pi 3.


## Tabla de Contenido 📄
1. [Arquitectura](#architecture)
2. [Instalación](#installation)
3. [Modo de Uso](#usage)
4. [Base de Datos](#database)
5. [Tecnlogias](#technologies)
6. [Autores](#authors)


## Arquitectura 🛠️
### Diseño de la Arquitectura ✒️
<!-- img -->
<img src="img/Architecture.png" alt="architecture" width="500" style="border-radius: 8px;"/>

### Componentes Hardware 📌
- Raspberry Pi 3
- Arduino UNO
- Sensor MFRC-522 o Modulo RFID-RC522
- Tags RFID

### Esquema de Conexión 🔖

Este esquema de conexión es para el sensor RFID-RC522.
<!-- img -->
<img src="img/RFID_Schema_image.png" alt="connection" width="500" style="border-radius: 8px;"/>

## Instalación 🔧
### Requisitos del proyecto 🪛
- Python 3.10
- Arduino IDE
- XAMPP(para pruebas locales)
- Postman(para pruebas locales de la API)
- PostgreSQL
- AWS (para despliegue en la nube)
- Node.js
- Raspberry Pi 3
- Sensor RFID-RC522
- Arduino UNO
- Tags RFID

### Pasos de Instalación 🪜
1. **Construir el esquema de conexión**
<!-- img -->
<img src="img/1paso.jfif" alt="connection" width="500" style="border-radius: 8px;"/>

2. **Ejecutar Codigo Arduino**
   * Instalar la libreria `MFRC522` de GithubCommunity en el IDE de Arduino.
   * Abrir el archivo `RFID.ino` y cargarlo en el Arduino UNO

```c
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9                 // Pin 9 para el reset del RC522
#define SS_PIN 10                 // Pin 10 para el SS (SDA) del RC522
MFRC522 mfrc522(SS_PIN, RST_PIN); // Creamos el objeto para el RC522

void setup()
{
  Serial.begin(9600); // Iniciamos la comunicación  serial
  SPI.begin();        // Iniciamos el Bus SPI
  mfrc522.PCD_Init(); // Iniciamos  el MFRC522
  Serial.println("Lectura del UID");
}

void loop()
{
  // Revisamos si hay nuevas tarjetas  presentes
  if (mfrc522.PICC_IsNewCardPresent())
  {
    // Seleccionamos una tarjeta
    if (mfrc522.PICC_ReadCardSerial())
    {
      // Enviamos serialemente su UID
      Serial.print("Card UID:");
      for (byte i = 0; i < mfrc522.uid.size; i++)
      {
        Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(mfrc522.uid.uidByte[i], HEX);
      }
      Serial.println();
      // Terminamos la lectura de la tarjeta  actual
      mfrc522.PICC_HaltA();
    }
  }
}
```

3. **Clonar el repositorio del Backend**
```bash
# Clonar el repositorio
$ git clone https://github.com/project-iot-fup/Backend
$ cd Backend
# Instalar el entorno virtual
$ pip install virtualenv
$ python -m virtualenv env
# Activar el entorno virtual en Linux
$ source env/bin/activate
# Activar el entorno virtual en Windows
$ env\Scripts\activate
# Instalar las dependencias
$ cd backend
$ pip install -r requirements.txt
# Solo si se tiene cuenta en AWS y ya se tiene configurado el Settings.py
$ python manage.py collectstatic
# Para migrar las tablas a la base de datos
$ python manage.py makemigrations
$ python manage.py migrate
# Correr proyecto
$ python manage.py runserver
```

**⚠️**: Para correr el proyecto en modo de desarrollo, se debe tener instalado XAMPP o PostgreSQL y crear una base de datos llamada `iot` en el phpmyadmin o en el pgadmin respectivamente.

**🎉**: Para correr el proyecto en modo de producción, se debe tener una cuenta en AWS y crear una instancia de RDS con PostgreSQL y de igual manera crear una base de datos llamada `iot`, para luego configurar las variables de entorno en el archivo `.env` del proyecto.

```bash
# Variables de entorno
AWS_ACCESS_KEY_ID='your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'
```

```python
# settings.py

# AWS settings
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
}

# No olvide restablecer la conexión de la base de datos y ocultar la contraseña

# Almacena los archivos estáticos en S3 en la carpeta "static"

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/images/'
```

4. **Clonar el repositorio del Frontend**
```bash
# Clonar el repositorio
$ git clone https://github.com/project-iot-fup/Frontend
$ cd Frontend
# Instalar las dependencias
$ npm install
# Correr proyecto
$ npm start
```



## Modo de Uso 📋

1. El estudiante se acerca al sensor RFID y coloca su tarjeta.
2. El sensor RFID envia la información de la tarjeta al Arduino.
3. El Arduino envia la información de la tarjeta al Raspberry Pi.
4. Si la tarjeta esta relacionada con un estudiante, debe validar la información de la tarjeta con la base de datos, además confirmar si el estudiante pertenece a dicha clase.
5. Luego se muestra la información del estudiante en la pantalla del docente, y se registra la asistencia en la base de datos.


## Base de Datos 💽






## Tecnlogias 🧰
En este proyecto se usaron las siguientes tecnologias:
* [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/): Version 3 de la Raspberry Pi.
* [PostgreSQL](https://www.postgresql.org/): Sistema de gestión de base de datos relacional.
* [Python](https://www.python.org/): Version 3.10.7
* [React](https://reactjs.org/): Version 18.2.0
* [Django](https://www.djangoproject.com/): Version 4.1.0
* [TailwindCSS](https://tailwindcss.com/): Version 3.1.8
* [Postman](https://www.postman.com/): Version 9.1.5
* [XAMPP](https://www.apachefriends.org/es/index.html): Version 8.0.11
* [Arduino](https://www.arduino.cc/): Version 2.0.0
* [Fritzing](https://fritzing.org/): Version 0.9.6

## Contribuciones 🖇️

```bash
# Materia: Creditos Libres II
$ Manuel Esteban Erazo
$ Jose Domingo Aranda Calambas
$ Jhon Leon
```

## Licencia MIT ⚖️

Este proyecto está bajo la Licencia (MIT) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

***