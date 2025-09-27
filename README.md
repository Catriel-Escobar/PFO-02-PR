# Sistema de Gestión de Tareas con API y Base de Datos

Este proyecto implementa un sistema de gestión de tareas con una API REST y base de datos SQLite. Permite el registro de usuarios, inicio de sesión y visualización de una página de bienvenida.

## Requisitos

- Python 3.6 o superior
- Flask
- Werkzeug

## Instalación

1. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

2. Clona o descarga este repositorio en tu máquina local.

## Estructura del Proyecto

```
proyecto/
│
├── servidor.py         # Servidor API Flask
├── cliente.py          # Cliente en consola para interactuar con la API
├── tareas.db           # Base de datos SQLite (se crea automáticamente)
├── requirements.txt    # Dependencias del proyecto
└── templates/
    └── bienvenida.html # Plantilla HTML para la página de bienvenida
```

## Ejecución

### Servidor

1. Navega hasta el directorio del proyecto:

```bash
cd ruta/al/proyecto
```

2. Ejecuta el servidor en una terminal:

```bash
python servidor.py
```

El servidor se iniciará en `http://127.0.0.1:5000/`.

### Cliente en Consola

3. En otra terminal, ejecuta el cliente:

```bash
python cliente.py
```

El cliente te permitirá interactuar con la API a través de una interfaz de consola amigable.

## Uso de la API

### Registro de Usuarios

- **Endpoint**: `POST /registro`
- **Cuerpo de la solicitud**:
  ```json
  {
    "usuario": "nombre_usuario",
    "contraseña": "contraseña_segura"
  }
  ```
- **Respuesta exitosa** (código 201):
  ```json
  {
    "mensaje": "Usuario registrado correctamente"
  }
  ```

### Inicio de Sesión

- **Endpoint**: `POST /login`
- **Cuerpo de la solicitud**:
  ```json
  {
    "usuario": "nombre_usuario",
    "contraseña": "contraseña_segura"
  }
  ```
- **Respuesta exitosa** (código 200):
  ```json
  {
    "mensaje": "Inicio de sesión exitoso",
    "usuario_id": 1
  }
  ```

### Página de Bienvenida

- **Endpoint**: `GET /tareas`
- **Respuesta**: Página HTML de bienvenida

## Pruebas

Puedes probar la API utilizando herramientas como [Postman](https://www.postman.com/) o [curl](https://curl.se/).

### Ejemplo con curl

1. Registrar un usuario:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"usuario\":\"test\",\"contraseña\":\"1234\"}" http://127.0.0.1:5000/registro
```

2. Iniciar sesión:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"usuario\":\"test\",\"contraseña\":\"1234\"}" http://127.0.0.1:5000/login
```

3. Acceder a la página de bienvenida:

```bash
curl http://127.0.0.1:5000/tareas
```

## Cliente en Consola

El cliente en consola (`cliente.py`) proporciona una interfaz amigable para interactuar con la API:

### Funcionalidades:

- **Registro de usuarios**: Crear nuevas cuentas de usuario
- **Inicio de sesión**: Autenticarse en el sistema
- **Visualización de página de bienvenida**: Ver el contenido HTML renderizado en consola
- **Gestión de sesiones**: Mantener sesiones activas y cerrarlas

### Uso:

1. Ejecuta `python cliente.py`
2. Selecciona las opciones del menú usando números
3. Sigue las instrucciones en pantalla
4. El cliente verificará automáticamente la conexión con el servidor

### Características técnicas:

- Interfaz de consola intuitiva con menús
- Manejo de errores robusto
- Verificación de conectividad con el servidor
- Conversión de HTML a texto legible en consola
- Gestión de sesiones HTTP

## Seguridad

- Las contraseñas se almacenan hasheadas utilizando la librería Werkzeug.
- Nunca se almacenan contraseñas en texto plano.

## Características

- API REST con endpoints funcionales
- Autenticación básica con protección de contraseñas
- Persistencia de datos con SQLite
- Página de bienvenida HTML
- Cliente en consola para interactuar con la API
