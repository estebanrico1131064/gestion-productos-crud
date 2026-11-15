"""Modelo de dominio del registro de productos."""

from dataclasses import asdict
from dataclasses import dataclass


@dataclass
class Producto:
    """Representa un producto del inventario.

    Atributos:
        id: Identificador unico y autoincremental del producto.
        nombre: Nombre comercial del producto.
        descripcion: Breve descripcion del producto.
        precio: Precio unitario en pesos.
        cantidad: Unidades disponibles en inventario.
    """

    id: int
    nombre: str
    descripcion: str
    precio: float
    cantidad: int

    def a_diccionario(self) -> dict:
        """Convierte el producto en un diccionario serializable a JSON."""
        return asdict(self)

    @classmethod
    def desde_diccionario(cls, datos: dict) -> "Producto":
        """Construye un producto a partir de un diccionario leido del JSON."""
        return cls(
            id=int(datos["id"]),
            nombre=str(datos["nombre"]),
            descripcion=str(datos.get("descripcion", "")),
            precio=float(datos["precio"]),
            cantidad=int(datos["cantidad"]),
        )

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.nombre} | {self.descripcion} | "
            f"precio: ${self.precio:,.2f} | cantidad: {self.cantidad}"
        )
