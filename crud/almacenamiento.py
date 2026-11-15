"""Persistencia del inventario en un archivo JSON."""

import json
from pathlib import Path

from .errores import ErrorDeAlmacenamiento


class AlmacenamientoJSON:
    """Lee y escribe listas de productos en un archivo JSON.

    La escritura se hace sobre un archivo temporal y luego se reemplaza el
    original, de modo que una falla a mitad de la escritura no corrompe los
    datos ya guardados.
    """

    def __init__(self, ruta: str | Path) -> None:
        self.ruta = Path(ruta)

    def cargar(self) -> list[dict]:
        """Devuelve la lista de productos guardada (vacia si no existe el archivo)."""
        if not self.ruta.exists():
            return []

        try:
            with self.ruta.open(encoding="utf-8") as archivo:
                contenido = json.load(archivo)
        except (OSError, json.JSONDecodeError) as error:
            raise ErrorDeAlmacenamiento(
                f"No fue posible leer el archivo {self.ruta}: {error}"
            ) from error

        if not isinstance(contenido, list):
            raise ErrorDeAlmacenamiento(
                f"El archivo {self.ruta} debe contener una lista de productos."
            )
        return contenido

    def guardar(self, productos: list[dict]) -> None:
        """Escribe la lista de productos en disco de forma atomica."""
        try:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            temporal = self.ruta.with_suffix(self.ruta.suffix + ".tmp")
            with temporal.open("w", encoding="utf-8") as archivo:
                json.dump(productos, archivo, ensure_ascii=False, indent=2)
            temporal.replace(self.ruta)
        except OSError as error:
            raise ErrorDeAlmacenamiento(
                f"No fue posible escribir el archivo {self.ruta}: {error}"
            ) from error
