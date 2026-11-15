"""Excepciones propias del dominio de productos."""


class ErrorDeProductos(Exception):
    """Excepcion base para todos los errores del CRUD de productos."""


class DatosInvalidosError(ErrorDeProductos):
    """Se lanza cuando los datos de un producto no cumplen las validaciones."""


class ProductoNoEncontradoError(ErrorDeProductos):
    """Se lanza cuando se busca un producto con un id que no existe."""


class ErrorDeAlmacenamiento(ErrorDeProductos):
    """Se lanza cuando el archivo de persistencia no se puede leer o escribir."""
