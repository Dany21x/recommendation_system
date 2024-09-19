# Product Recommendation API

Esta es una API para gestionar usuarios, productos y preferencias de categorías de productos, así como generar recomendaciones personalizadas para los usuarios. El proyecto ha sido probado en Python3.12

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
pip install -r requirements.txt
```
### 3. Crear archivo .env 
Con parámetro DATABASE_URL asociado a la base de datos en postgres (en caso de que dicho archivo no exista)

### 4. Crear esquema recommendation_system en la base de datos postgres

### 5. En el cmd donde tenemos el entorno virtual activo, ejecutar 
```bash
uvicorn app.main:app --reload --port 3001
```

### 6. Datos cargados automáticamente

Con el objetivo de facilitar las pruebas de la API, en el archivo principal main.py se ejecuta automáticamente la función "populate_data" la cual llena las tablas con información cargada en archivos .csv

## Acceso a la documentación de la API

Para ver la documentación de la API y ejemplos de uso de sus endpoints, abre un navegador web y navega a la siguiente URL:
```bash
http:localhost:3001/docs 
```
(O el puerto donde esté corriendo la aplicación FastAPI)

Con esto se accede a la documentación interactiva generada automáticamente por FastAPI, basada en Swagger UI.