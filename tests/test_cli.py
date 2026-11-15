"""Pruebas unitarias de la capa de consola (main.py)."""

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import main
from crud import GestorProductos, Producto, ProductoNoEncontradoError


class PruebaPedirDatos(unittest.TestCase):
    """Valida las funciones auxiliares que leen datos del usuario."""

    def test_pedir_texto_devuelve_el_valor_sin_espacios(self) -> None:
        with patch("builtins.input", return_value="  Teclado  "):
            self.assertEqual(main.pedir_texto("Nombre: "), "Teclado")

    def test_pedir_texto_repite_cuando_el_campo_es_obligatorio(self) -> None:
        with patch("builtins.input", side_effect=["", "   ", "Mouse"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main.pedir_texto("Nombre: "), "Mouse")

    def test_pedir_texto_opcional_acepta_vacio(self) -> None:
        with patch("builtins.input", return_value=""):
            self.assertEqual(main.pedir_texto("Descripcion: ", obligatorio=False), "")

    def test_pedir_numero_convierte_el_tipo_solicitado(self) -> None:
        with patch("builtins.input", return_value="42"):
            self.assertEqual(main.pedir_numero("Cantidad: ", int), 42)
        with patch("builtins.input", return_value="1500.5"):
            self.assertEqual(main.pedir_numero("Precio: ", float), 1500.5)

    def test_pedir_numero_repite_cuando_el_valor_es_invalido(self) -> None:
        with patch("builtins.input", side_effect=["abc", "7"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main.pedir_numero("Cantidad: ", int), 7)


class PruebaOpcionesDelMenu(unittest.TestCase):
    """Ejercita cada opcion del menu sobre un almacenamiento temporal."""

    def setUp(self) -> None:
        self._carpeta = TemporaryDirectory()
        self.ruta = Path(self._carpeta.name) / "productos.json"
        self.gestor = GestorProductos(self.ruta)

    def tearDown(self) -> None:
        self._carpeta.cleanup()

    def _producto_de_ejemplo(self) -> Producto:
        return self.gestor.crear("Teclado", "USB", 150000, 10)

    def test_mostrar_producto_imprime_sus_datos(self) -> None:
        producto = Producto(1, "Mouse", "Optico", 80000.0, 5)
        salida = io.StringIO()

        with redirect_stdout(salida):
            main.mostrar_producto(producto)

        self.assertIn("Mouse", salida.getvalue())
        self.assertIn("80,000.00", salida.getvalue())

    def test_crear_desde_el_menu(self) -> None:
        salida = io.StringIO()

        with patch("builtins.input", side_effect=["Monitor", "24 pulgadas", "900000", "3"]):
            with redirect_stdout(salida):
                main.crear(self.gestor)

        self.assertEqual(len(self.gestor.listar()), 1)
        self.assertIn("creado con id 1", salida.getvalue())

    def test_listar_sin_productos_lo_indica(self) -> None:
        salida = io.StringIO()

        with redirect_stdout(salida):
            main.listar(self.gestor)

        self.assertIn("No hay productos registrados", salida.getvalue())

    def test_listar_con_productos_muestra_el_total(self) -> None:
        self._producto_de_ejemplo()
        salida = io.StringIO()

        with redirect_stdout(salida):
            main.listar(self.gestor)

        self.assertIn("Total: 1 producto", salida.getvalue())

    def test_buscar_por_id(self) -> None:
        producto = self._producto_de_ejemplo()
        salida = io.StringIO()

        with patch("builtins.input", return_value=str(producto.id)):
            with redirect_stdout(salida):
                main.buscar_por_id(self.gestor)

        self.assertIn("Teclado", salida.getvalue())

    def test_buscar_por_texto_sin_resultados(self) -> None:
        self._producto_de_ejemplo()
        salida = io.StringIO()

        with patch("builtins.input", return_value="impresora"):
            with redirect_stdout(salida):
                main.buscar_por_texto(self.gestor)

        self.assertIn("No se encontraron coincidencias", salida.getvalue())

    def test_actualizar_desde_el_menu(self) -> None:
        producto = self._producto_de_ejemplo()

        with patch(
            "builtins.input",
            side_effect=[str(producto.id), "Teclado inalambrico", "", "0", "20"],
        ), redirect_stdout(io.StringIO()):
            main.actualizar(self.gestor)

        actualizado = self.gestor.leer(producto.id)
        self.assertEqual(actualizado.nombre, "Teclado inalambrico")
        self.assertEqual(actualizado.cantidad, 20)
        self.assertEqual(actualizado.precio, 150000.0, "El precio 0 conserva el valor")

    def test_eliminar_desde_el_menu(self) -> None:
        producto = self._producto_de_ejemplo()

        with patch("builtins.input", return_value=str(producto.id)):
            with redirect_stdout(io.StringIO()):
                main.eliminar(self.gestor)

        self.assertEqual(self.gestor.listar(), [])

    def test_eliminar_un_id_inexistente_propaga_el_error(self) -> None:
        with patch("builtins.input", return_value="999"):
            with redirect_stdout(io.StringIO()):
                with self.assertRaises(ProductoNoEncontradoError):
                    main.eliminar(self.gestor)


class PruebaBuclePrincipal(unittest.TestCase):
    """Valida el arranque y la salida del menu principal."""

    def test_main_sale_al_elegir_cero(self) -> None:
        salida = io.StringIO()

        with patch("builtins.input", return_value="0"), redirect_stdout(salida):
            main.main()

        self.assertIn("Hasta pronto", salida.getvalue())

    def test_main_informa_una_opcion_no_valida(self) -> None:
        salida = io.StringIO()

        with patch("builtins.input", side_effect=["9", "0"]), redirect_stdout(salida):
            main.main()

        self.assertIn("Opcion no valida", salida.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
