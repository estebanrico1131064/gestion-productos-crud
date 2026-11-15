# Gestion de Productos - CRUD en Python

Taller evaluativo de la Guia de Trabajo No. 4 de **Aplicaciones y Servicios Web**
(Instituto Tecnologico Metropolitano).

Aplicacion de consola que implementa las operaciones **Crear, Leer, Actualizar y
Eliminar** sobre un registro de productos, con persistencia en un archivo JSON y
pruebas unitarias con `unittest`.

## Requisitos

- Python 3.10 o superior
- No requiere dependencias externas para ejecutar la aplicacion

## Estructura del proyecto

```
.
|-- main.py                     # Menu interactivo (punto de entrada)
|-- crud/
|   |-- __init__.py             # Expone las clases publicas del paquete
|   |-- modelo.py               # Entidad Producto (id, nombre, descripcion, precio, cantidad)
|   |-- almacenamiento.py       # Persistencia en archivo JSON
|   |-- servicio.py             # Logica del CRUD y validaciones
|   `-- errores.py              # Excepciones propias del dominio
|-- tests/
|   `-- test_crud.py            # Pruebas unitarias (caso exitoso y de error por operacion)
|-- data/
|   `-- productos.json          # Se crea automaticamente al primer registro
|-- sonar-project.properties    # Configuracion del analisis de calidad
|-- requirements.txt
`-- README.md
```

## Uso

```bash
python main.py
```

El menu permite:

1. Crear producto
2. Listar productos
3. Buscar producto por id
4. Buscar producto por texto
5. Actualizar producto
6. Eliminar producto
0. Salir

## Pruebas unitarias

```bash
python -m unittest discover -s tests -v
```

Para generar el reporte de cobertura que consume SonarQube:

```bash
pip install coverage
coverage run -m unittest discover -s tests
coverage xml
```

## Analisis de calidad con SonarQube Cloud

El proyecto incluye el flujo de trabajo `.github/workflows/sonarqube.yml`, que
ejecuta las pruebas con cobertura y envia el analisis a SonarQube Cloud en cada
`push`. Para activarlo:

1. Crear la organizacion y el proyecto en <https://sonarcloud.io> vinculados a GitHub.
2. Agregar el token del proyecto como secreto `SONAR_TOKEN` en el repositorio.
3. Ajustar `sonar.organization` y `sonar.projectKey` en `sonar-project.properties`.

## Autor

Esteban Rico - [estebanrico1131064](https://github.com/estebanrico1131064)

Repositorio: <https://github.com/estebanrico1131064/gestion-productos-crud>

Instituto Tecnologico Metropolitano - Aplicaciones y Servicios Web
