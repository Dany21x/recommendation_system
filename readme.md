# Product Recommendation API

Esta es una API para gestionar usuarios, productos y preferencias de categorías de productos, así como generar recomendaciones personalizadas para los usuarios.

## Pasos para configurar el proyecto

### 1. Crear y activar el entorno virtual
Es recomendable trabajar con un entorno virtual para manejar las dependencias del proyecto. Para crear y activar el entorno virtual, ejecuta los siguientes comandos según tu sistema operativo:

#### En Windows:
```bash
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate
```
### 2. Instalar librerías

```bash
pip -r requirements.txt
```
### 3. Crear archivo .env con parámetro DATABASE_URL asociado a la base de datos en postgres

### 4. Crear esquema recommendation_system en la base de datos postgres

### 5. En el cmd donde tenemos el entorno virtual activo, ejecutar 
```bash
uvicorn app.main:app --reload --port 5001
```

## Acceso a la documentación de la API

Para ver la documentación de la API y ejemplos de uso de sus endpoints, abre un navegador web y navega a la siguiente URL:
```bash
http:localhost:5001/docs 
```
(O el puerto donde esté corriendo la aplicación FastAPI)

Con esto se accede a la documentación interactiva generada automáticamente por FastAPI, basada en Swagger UI.