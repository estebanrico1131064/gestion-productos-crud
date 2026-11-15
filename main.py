"""Punto de entrada: menu interactivo del CRUD de productos."""

from pathlib import Path

from crud import ErrorDeProductos, GestorProductos, Producto

RUTA_DATOS = Path(__file__).parent / "data" / "productos.json"

MENU = """
==================================================
     GESTION DE PRODUCTOS - CRUD EN PYTHON
==================================================
 1. Crear producto
 2. Listar productos
 3. Buscar producto por id
 4. Buscar producto por texto
 5. Actualizar producto
 6. Eliminar producto
 0. Salir
==================================================
"""


def pedir_texto(mensaje: str, obligatorio: bool = True) -> str:
    """Solicita un texto por consola y valida que no venga vacio."""
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("  [!] Este campo es obligatorio, intenta de nuevo.")


def pedir_numero(mensaje: str, tipo: type):
    """Solicita un numero por consola y valida el tipo indicado."""
    while True:
        valor = input(mensaje).strip()
        try:
            return tipo(valor)
        except ValueError:
            print(f"  [!] Valor invalido, se esperaba un dato de tipo {tipo.__name__}.")


def mostrar_producto(producto: Producto) -> None:
    """Imprime un producto con formato de tabla simple."""
    print(f"  {producto}")


def crear(gestor: GestorProductos) -> None:
    print("\n--- CREAR PRODUCTO ---")
    nombre = pedir_texto("Nombre: ")
    descripcion = pedir_texto("Descripcion: ", obligatorio=False)
    precio = pedir_numero("Precio: ", float)
    cantidad = pedir_numero("Cantidad: ", int)

    producto = gestor.crear(nombre, descripcion, precio, cantidad)
    print(f"\n  [OK] Producto creado con id {producto.id}.")
    mostrar_producto(producto)


def listar(gestor: GestorProductos) -> None:
    print("\n--- LISTADO DE PRODUCTOS ---")
    productos = gestor.listar()
    if not productos:
        print("  No hay productos registrados.")
        return
    for producto in productos:
        mostrar_producto(producto)
    print(f"\n  Total: {len(productos)} producto(s).")


def buscar_por_id(gestor: GestorProductos) -> None:
    print("\n--- BUSCAR PRODUCTO POR ID ---")
    id_producto = pedir_numero("Id: ", int)
    mostrar_producto(gestor.leer(id_producto))


def buscar_por_texto(gestor: GestorProductos) -> None:
    print("\n--- BUSCAR PRODUCTO POR TEXTO ---")
    texto = pedir_texto("Texto a buscar: ")
    resultados = gestor.buscar(texto)
    if not resultados:
        print("  No se encontraron coincidencias.")
        return
    for producto in resultados:
        mostrar_producto(producto)


def actualizar(gestor: GestorProductos) -> None:
    print("\n--- ACTUALIZAR PRODUCTO ---")
    id_producto = pedir_numero("Id del producto a actualizar: ", int)
    gestor.leer(id_producto)
    print("  Deja el campo vacio para conservar el valor actual.")

    nombre = pedir_texto("Nuevo nombre: ", obligatorio=False)
    descripcion = pedir_texto("Nueva descripcion: ", obligatorio=False)
    precio = pedir_numero("Nuevo precio (0 = conservar): ", float)
    cantidad = pedir_numero("Nueva cantidad (-1 = conservar): ", int)

    producto = gestor.actualizar(
        id_producto,
        nombre=nombre or None,
        descripcion=descripcion or None,
        precio=precio if precio != 0 else None,
        cantidad=cantidad if cantidad != -1 else None,
    )
    print("\n  [OK] Producto actualizado.")
    mostrar_producto(producto)


def eliminar(gestor: GestorProductos) -> None:
    print("\n--- ELIMINAR PRODUCTO ---")
    id_producto = pedir_numero("Id del producto a eliminar: ", int)
    producto = gestor.eliminar(id_producto)
    print(f"\n  [OK] Producto eliminado: {producto.nombre}")


ACCIONES = {
    "1": crear,
    "2": listar,
    "3": buscar_por_id,
    "4": buscar_por_texto,
    "5": actualizar,
    "6": eliminar,
}


def main() -> None:
    """Ejecuta el menu principal hasta que el usuario decida salir."""
    gestor = GestorProductos(RUTA_DATOS)
    while True:
        print(MENU)
        opcion = input("Selecciona una opcion: ").strip()
        if opcion == "0":
            print("\nHasta pronto.")
            return
        accion = ACCIONES.get(opcion)
        if accion is None:
            print("\n  [!] Opcion no valida.")
            continue
        try:
            accion(gestor)
        except ErrorDeProductos as error:
            print(f"\n  [ERROR] {error}")
        except ValueError as error:
            print(f"\n  [ERROR] {error}")


if __name__ == "__main__":
    main()
