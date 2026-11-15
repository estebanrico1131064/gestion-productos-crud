"""Logica de negocio del CRUD de productos."""

from pathlib import Path

from .almacenamiento import AlmacenamientoJSON
from .errores import DatosInvalidosError, ProductoNoEncontradoError
from .modelo import Producto


class GestorProductos:
    """Administra el ciclo de vida (CRUD) de los productos.

    Los datos se mantienen en memoria y se sincronizan con un archivo JSON
    cada vez que se crea, actualiza o elimina un producto.
    """

    def __init__(self, ruta_almacenamiento: str | Path = "data/productos.json") -> None:
        self._almacenamiento = AlmacenamientoJSON(ruta_almacenamiento)
        self._productos: list[Producto] = [
            Producto.desde_diccionario(datos)
            for datos in self._almacenamiento.cargar()
        ]

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def crear(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
        cantidad: int,
    ) -> Producto:
        """Registra un producto nuevo y le asigna el siguiente id disponible.

        Lanza:
            DatosInvalidosError: si alguno de los campos no cumple las reglas.
        """
        nombre = self._validar_nombre(nombre)
        descripcion = self._validar_descripcion(descripcion)
        precio = self._validar_precio(precio)
        cantidad = self._validar_cantidad(cantidad)

        producto = Producto(
            id=self._siguiente_id(),
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=cantidad,
        )
        self._productos.append(producto)
        self._guardar()
        return producto

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def listar(self) -> list[Producto]:
        """Devuelve todos los productos registrados."""
        return list(self._productos)

    def leer(self, id_producto: int) -> Producto:
        """Devuelve el producto con el id indicado.

        Lanza:
            ProductoNoEncontradoError: si el id no existe en el inventario.
        """
        return self._buscar(id_producto)

    def buscar(self, texto: str) -> list[Producto]:
        """Devuelve los productos cuyo nombre o descripcion contienen el texto."""
        texto_busqueda = texto.strip().lower()
        if not texto_busqueda:
            return self.listar()
        return [
            producto
            for producto in self._productos
            if texto_busqueda in producto.nombre.lower()
            or texto_busqueda in producto.descripcion.lower()
        ]

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def actualizar(
        self,
        id_producto: int,
        nombre: str | None = None,
        descripcion: str | None = None,
        precio: float | None = None,
        cantidad: int | None = None,
    ) -> Producto:
        """Modifica los campos enviados del producto y conserva el resto.

        Lanza:
            ProductoNoEncontradoError: si el id no existe.
            DatosInvalidosError: si los nuevos valores no cumplen las reglas.
        """
        producto = self._buscar(id_producto)

        if nombre is not None:
            producto.nombre = self._validar_nombre(nombre)
        if descripcion is not None:
            producto.descripcion = self._validar_descripcion(descripcion)
        if precio is not None:
            producto.precio = self._validar_precio(precio)
        if cantidad is not None:
            producto.cantidad = self._validar_cantidad(cantidad)

        self._guardar()
        return producto

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def eliminar(self, id_producto: int) -> Producto:
        """Quita del inventario el producto con el id indicado.

        Lanza:
            ProductoNoEncontradoError: si el id no existe.
        """
        producto = self._buscar(id_producto)
        self._productos.remove(producto)
        self._guardar()
        return producto

    # ------------------------------------------------------------------
    # Apoyo interno
    # ------------------------------------------------------------------
    def _buscar(self, id_producto: int) -> Producto:
        for producto in self._productos:
            if producto.id == id_producto:
                return producto
        raise ProductoNoEncontradoError(
            f"No existe un producto con id {id_producto}."
        )

    def _siguiente_id(self) -> int:
        if not self._productos:
            return 1
        return max(producto.id for producto in self._productos) + 1

    def _guardar(self) -> None:
        self._almacenamiento.guardar(
            [producto.a_diccionario() for producto in self._productos]
        )

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del producto es obligatorio.")
        if len(nombre.strip()) > 100:
            raise DatosInvalidosError("El nombre no puede superar 100 caracteres.")
        return nombre.strip()

    @staticmethod
    def _validar_descripcion(descripcion: str) -> str:
        if not isinstance(descripcion, str):
            raise DatosInvalidosError("La descripcion debe ser un texto.")
        if len(descripcion.strip()) > 250:
            raise DatosInvalidosError("La descripcion no puede superar 250 caracteres.")
        return descripcion.strip()

    @staticmethod
    def _validar_precio(precio: float) -> float:
        if isinstance(precio, bool) or not isinstance(precio, (int, float)):
            raise DatosInvalidosError("El precio debe ser un numero.")
        precio = float(precio)
        if precio < 0:
            raise DatosInvalidosError("El precio no puede ser negativo.")
        return round(precio, 2)

    @staticmethod
    def _validar_cantidad(cantidad: int) -> int:
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise DatosInvalidosError("La cantidad debe ser un numero entero.")
        if cantidad < 0:
            raise DatosInvalidosError("La cantidad no puede ser negativa.")
        return cantidad
