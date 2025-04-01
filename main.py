import os
import time
import json
from modelo.cliente import Cliente
from modelo.factura import Factura
from modelo.plagas import ControlPlagas
from modelo.fertilizantes import ControlFertilizantes
from modelo.antibiotico import Antibiotico

#Diccionarios
clientes = {}
facturas = []
productos = []

#Archivos json
CLIENTES_FILE = "clientes.json"
FACTURAS_FILE = "facturas.json"
PRODUCTOS_FILE = "productos.json"

def guardar_datos():
    #Utilizamos un archivo json para tener mayor facilidad a la hora de maniobrar datos que con el txt de toda la vida
    with open(CLIENTES_FILE, "w") as file:
        json.dump({cedula: {"nombre": cliente.nombre, "cedula": cliente.cedula} for cedula, cliente in clientes.items()}, file, indent=4)
    
    with open(FACTURAS_FILE, "w") as file:
        json.dump([{
            "cliente": factura.cliente.cedula,
            "productos": [{"nombre": p.nombre, "precio": p.precio} for p in factura.productos],
            "total": factura.total
        } for factura in facturas], file, indent=4)
    
    with open(PRODUCTOS_FILE, "w") as file:
        json.dump([{"nombre": p.nombre, "precio": p.precio} for p in productos], file, indent=4)

def cargar_datos():
    global clientes, facturas, productos
    
    if os.path.exists(CLIENTES_FILE):
        with open(CLIENTES_FILE, "r") as file:
            datos_clientes = json.load(file)
            clientes = {cedula: Cliente(data["nombre"], data["cedula"]) for cedula, data in datos_clientes.items()}
    
    if os.path.exists(FACTURAS_FILE):
        with open(FACTURAS_FILE, "r") as file:
            datos_facturas = json.load(file)
            for data in datos_facturas:
                cliente = clientes.get(data["cliente"])
                if cliente:
                    factura = Factura(cliente)
                    for p in data["productos"]:
                        producto = ControlPlagas(p["nombre"], p["precio"], "N/A", "N/A", 0)  # Carga básica
                        factura.agregar_producto(producto)
                    facturas.append(factura)
    
    if os.path.exists(PRODUCTOS_FILE):
        with open(PRODUCTOS_FILE, "r") as file:
            datos_productos = json.load(file)
            productos = [ControlPlagas(p["nombre"], p["precio"], "N/A", "N/A", 0) for p in datos_productos]  # Carga básica

def salir():
    print("Guardando datos...")
    guardar_datos()
    print("Datos guardados. Saliendo del sistema...")

cargar_datos()

#utilizamos la libreria os para manipular el cmd
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """Pausa la ejecución antes de limpiar la pantalla."""
    print("\nPresione Enter para continuar...")
    input()
    time.sleep(0.5)
    limpiar_pantalla()

#al registrar tambien se verifica que existan otros clientes con la misma cedula
def registrar_cliente():
    limpiar_pantalla()
    nombre = input("Nombre del Cliente: ")
    cedula = input("Cédula del Cliente: ")
    if cedula in clientes:
        print("\nEste cliente ya está registrado.")
    else:
        clientes[cedula] = Cliente(nombre, cedula)
        print(f"\nCliente {nombre} registrado con éxito.")
    pausar()

#Creamos la factura teniendo en cuenta los 3 tipos de productos
def crear_factura():
    limpiar_pantalla()
    cedula = input("Ingrese la cédula del cliente: ")
    if cedula not in clientes:
        print("\nCliente no encontrado. Regístrelo primero.")
        pausar()
        return

    cliente = clientes[cedula]
    factura = Factura(cliente)

    while True:
        limpiar_pantalla()
        print("\n--- AGREGAR PRODUCTO ---")
        print("1. Control de Plagas")
        print("2. Control de Fertilizantes")
        print("3. Antibiótico")
        print("4. Finalizar Factura")
        opcion_producto = input("Seleccione una opción: ")

        if opcion_producto == "1":
            limpiar_pantalla()
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            registro_ica = input("Registro ICA: ")
            frecuencia = input("Frecuencia de aplicación: ")
            periodo_carencia = int(input("Periodo de carencia (días): "))
            producto = ControlPlagas(nombre, precio, registro_ica, frecuencia, periodo_carencia)

        elif opcion_producto == "2":
            limpiar_pantalla()
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            registro_ica = input("Registro ICA: ")
            frecuencia = input("Frecuencia de aplicación: ")
            fecha_ultima = input("Fecha de última aplicación: ")
            producto = ControlFertilizantes(nombre, precio, registro_ica, frecuencia, fecha_ultima)

        elif opcion_producto == "3":
            limpiar_pantalla()
            nombre = input("Nombre del antibiótico: ")
            precio = float(input("Precio: "))
            dosis = input("Dosis (Kg): ")
            tipo_animal = input("Tipo de animal (Bovino/Caprino/Porcino): ")
            producto = Antibiotico(nombre, precio, dosis, tipo_animal)

        elif opcion_producto == "4":
            break
        
        else:
            print("Opción no válida.")
            pausar()
            continue

        factura.agregar_producto(producto)
        productos.append(producto) 
        print(f"\nProducto {producto.nombre} agregado.")
        pausar()

    cliente.agregar_factura(factura)
    facturas.append(factura) 
    limpiar_pantalla()

    print("\n--- FACTURA GENERADA ---")
    print(f"Cliente: {cliente.nombre}")
    print(f"Fecha: {factura.fecha}")
    print("\nProductos Comprados:")
    for producto in factura.productos:
        print(f"- {producto.nombre}: ${producto.precio:.2f}")
    print(f"\nTotal: ${factura.total:.2f}")

    pausar()

def ver_facturas():
    limpiar_pantalla()
    if not facturas:
        print("No hay facturas registradas.")
    else:
        print("\n--- TODAS LAS FACTURAS ---")
        for i, factura in enumerate(facturas, 1):
            print(f"\nFactura {i}:")
            print(f"Cliente: {factura.cliente.nombre}")
            print(f"Fecha: {factura.fecha}")
            print("Productos:")
            for producto in factura.productos:
                print(f"  - {producto.nombre}: ${producto.precio:.2f}")
            print(f"Total: ${factura.total:.2f}")
    pausar()

def ver_productos():
    limpiar_pantalla()
    if not productos:
        print("No hay productos registrados.")
    else:
        print("\n--- TODOS LOS PRODUCTOS ---")
        for i, producto in enumerate(productos, 1):
            print(f"{i}. {producto.nombre} - ${producto.precio:.2f}")
    pausar()

def ver_clientes():
    limpiar_pantalla()
    if not clientes:
        print("No hay clientes registrados.")
    else:
        print("\n--- TODOS LOS CLIENTES ---")
        for cedula, cliente in clientes.items():
            print(f"Nombre: {cliente.nombre}, Cédula: {cedula}")
    pausar()

def main():
    while True:
        print("\n--- SISTEMA DE FACTURACIÓN ---")
        print("1. Registrar Cliente")
        print("2. Crear Factura")
        print("3. Ver Todas las Facturas")
        print("4. Ver Todos los Productos")
        print("5. Ver Todos los Clientes")
        print("6. Guardar y Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            crear_factura()
        elif opcion == "3":
            ver_facturas()
        elif opcion == "4":
            ver_productos()
        elif opcion == "5":
            ver_clientes()
        elif opcion == "6":
            salir()
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
