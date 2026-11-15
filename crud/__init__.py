"""Paquete con la logica del CRUD de productos."""

from .errores import (
    DatosInvalidosError,
    ErrorDeAlmacenamiento,
    ErrorDeProductos,
    ProductoNoEncontradoError,
)
from .modelo import Producto
from .servicio import GestorProductos

__all__ = [
    "DatosInvalidosError",
    "ErrorDeAlmacenamiento",
    "ErrorDeProductos",
    "ProductoNoEncontradoError",
    "Producto",
    "GestorProductos",
]
