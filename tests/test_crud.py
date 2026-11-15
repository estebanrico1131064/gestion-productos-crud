"""Pruebas unitarias de las operaciones CRUD del gestor de productos."""

import json
import tempfile
import unittest
from pathlib import Path

from crud import (
    DatosInvalidosError,
    GestorProductos,
    ProductoNoEncontradoError,
)


class BasePruebaCRUD(unittest.TestCase):
    """Prepara un almacenamiento temporal y limpio para cada prueba."""

    def setUp(self) -> None:
        self._carpeta = tempfile.TemporaryDirectory()
        self.ruta = Path(self._carpeta.name) / "productos.json"
        self.gestor = GestorProductos(self.ruta)

    def tearDown(self) -> None:
        self._carpeta.cleanup()

    def crear_producto_ejemplo(self, **cambios) -> int:
        datos = {
            "nombre": "Teclado mecanico",
            "descripcion": "Teclado USB con switches azules",
            "precio": 150000,
            "cantidad": 10,
        }
        datos.update(cambios)
        return self.gestor.crear(**datos).id


class PruebaCrear(BasePruebaCRUD):
    """CREATE: un caso exitoso y varios casos de error."""

    def test_crear_producto_exitoso(self) -> None:
        producto = self.gestor.crear("Mouse gamer", "Mouse optico 1600 dpi", 80000, 5)

        self.assertEqual(producto.id, 1)
        self.assertEqual(producto.nombre, "Mouse gamer")
        self.assertEqual(producto.precio, 80000.0)
        self.assertEqual(producto.cantidad, 5)
        self.assertEqual(len(self.gestor.listar()), 1)

    def test_crear_asigna_ids_consecutivos(self) -> None:
        primero = self.crear_producto_ejemplo()
        segundo = self.crear_producto_ejemplo(nombre="Monitor 24 pulgadas")

        self.assertEqual((primero, segundo), (1, 2))

    def test_crear_con_nombre_vacio_lanza_error(self) -> None:
        with self.assertRaises(DatosInvalidosError):
            self.gestor.crear("   ", "Sin nombre", 1000, 1)

    def test_crear_con_precio_negativo_lanza_error(self) -> None:
        with self.assertRaises(DatosInvalidosError):
            self.gestor.crear("Diadema", "Diadema USB", -5000, 3)

    def test_crear_con_cantidad_negativa_lanza_error(self) -> None:
        with self.assertRaises(DatosInvalidosError):
            self.gestor.crear("Camara web", "Camara 1080p", 120000, -1)


class PruebaLeer(BasePruebaCRUD):
    """READ: un caso exitoso y varios casos de error."""

    def test_leer_producto_existente(self) -> None:
        id_producto = self.crear_producto_ejemplo()

        producto = self.gestor.leer(id_producto)

        self.assertEqual(producto.id, id_producto)
        self.assertEqual(producto.nombre, "Teclado mecanico")

    def test_listar_sin_productos_devuelve_lista_vacia(self) -> None:
        self.assertEqual(self.gestor.listar(), [])

    def test_leer_producto_inexistente_lanza_error(self) -> None:
        with self.assertRaises(ProductoNoEncontradoError):
            self.gestor.leer(999)

    def test_buscar_por_texto_sin_coincidencias_devuelve_lista_vacia(self) -> None:
        self.crear_producto_ejemplo()

        self.assertEqual(self.gestor.buscar("impresora"), [])


class PruebaActualizar(BasePruebaCRUD):
    """UPDATE: un caso exitoso y casos de error."""

    def test_actualizar_producto_existente(self) -> None:
        id_producto = self.crear_producto_ejemplo()

        producto = self.gestor.actualizar(
            id_producto, nombre="Teclado inalambrico", precio=175000
        )

        self.assertEqual(producto.nombre, "Teclado inalambrico")
        self.assertEqual(producto.precio, 175000.0)
        self.assertEqual(producto.cantidad, 10, "Los campos no enviados no cambian")

    def test_actualizar_producto_inexistente_lanza_error(self) -> None:
        with self.assertRaises(ProductoNoEncontradoError):
            self.gestor.actualizar(999, nombre="Producto fantasma")

    def test_actualizar_con_precio_invalido_lanza_error(self) -> None:
        id_producto = self.crear_producto_ejemplo()

        with self.assertRaises(DatosInvalidosError):
            self.gestor.actualizar(id_producto, precio=-1)


class PruebaEliminar(BasePruebaCRUD):
    """DELETE: un caso exitoso y un caso de error."""

    def test_eliminar_producto_existente(self) -> None:
        id_producto = self.crear_producto_ejemplo()

        eliminado = self.gestor.eliminar(id_producto)

        self.assertEqual(eliminado.id, id_producto)
        self.assertEqual(self.gestor.listar(), [])

    def test_eliminar_producto_inexistente_lanza_error(self) -> None:
        with self.assertRaises(ProductoNoEncontradoError):
            self.gestor.eliminar(999)


class PruebaPersistencia(BasePruebaCRUD):
    """Verifica que los cambios sobrevivan al cerrar y reabrir el gestor."""

    def test_los_productos_se_guardan_en_el_archivo_json(self) -> None:
        self.crear_producto_ejemplo()

        with self.ruta.open(encoding="utf-8") as archivo:
            contenido = json.load(archivo)

        self.assertEqual(len(contenido), 1)
        self.assertEqual(contenido[0]["nombre"], "Teclado mecanico")

    def test_un_nuevo_gestor_recupera_los_productos(self) -> None:
        id_producto = self.crear_producto_ejemplo()

        otro_gestor = GestorProductos(self.ruta)

        self.assertEqual(otro_gestor.leer(id_producto).nombre, "Teclado mecanico")


if __name__ == "__main__":
    unittest.main(verbosity=2)
