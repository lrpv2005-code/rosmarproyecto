# Rosmar Proyecto (Lenguaje de Programación 2)

Bienvenido al proyecto de reseñas de series desarrollado en Django.

## Requisitos
- Python (recomendado 3.10 o superior)
- Pip (Gestor de paquetes de Python)


# 0. ENTORNO VIRTUAL TE ODIO DANIEL DIOS

```bash
sudo apt install python3-venv
```
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

no hay explicación, ejecuta los comandos y luego sigue con el resto de pasos





##  1. Instalación de Dependencias

Antes de iniciar el servidor por primera vez, asegúrate de instalar las librerías necesarias. Abre una terminal o consola de comandos, asegúrate de estar dentro de la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

##  2. Iniciar el Servidor Web

Abre una terminal, asegúrate de estar dentro de la carpeta del proyecto y ejecuta el siguiente comando:

```bash
python manage.py runserver
```

Luego de ejecutarlo, abre tu navegador web de preferencia (Chrome, Edge, etc.) y entra a la siguiente dirección:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

##  3. Panel de Administración (Base de Datos)

El proyecto utiliza el potente panel de administración nativo de Django para gestionar la base de datos de manera visual e intuitiva.

Asegúrate de que el servidor esté corriendo. Luego, en una nueva pestaña del navegador, entra a:
[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Aparecerá un formulario donde te pedirán credenciales. Utiliza los siguientes datos configurados por defecto:

- **Usuario:** `admin`
- **Contraseña:** `admin123`

Una vez adentro, verás las siguientes secciones principales:
- **Series:** Aquí puedes ver las series, modificarlas o agregar nuevas.
- **Resenas:** Todas las calificaciones o reseñas hechas por los usuarios del sistema.
- **Users:** Lista con los usuarios que se han registrado en tu página. Las contraseñas están encriptadas automáticamente por seguridad.
