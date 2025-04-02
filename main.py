import tkinter as tk
from tkinter import messagebox
from modelo.cliente import Cliente
from modelo.factura import Factura
from modelo.plagas import ControlPlagas
from modelo.fertilizantes import ControlFertilizantes
from modelo.antibiotico import Antibiotico
import json
import os

# Diccionarios
clientes = {}
facturas = []
productos = []

# Archivos JSON
CLIENTES_FILE = "clientes.json"
FACTURAS_FILE = "facturas.json"
PRODUCTOS_FILE = "productos.json"

#Utilizamos un archivo json para tener mayor facilidad a la hora de maniobrar datos que con el txt de toda la vida
def guardar_datos():
    # Guardar clientes
    with open(CLIENTES_FILE, "w") as file:
        json.dump(
            {cedula: {"nombre": cliente.nombre, "cedula": cliente.cedula} 
             for cedula, cliente in clientes.items()}, file, indent=4
        )
    
    # Guardar facturas
    with open(FACTURAS_FILE, "w") as file:
        facturas_serializadas = []
        for factura in facturas:
            productos_serializados = []
            for p in factura.productos:
                #Determinamos el tipo de producto para guardarlo con sus caracteristicas.
                if isinstance(p, ControlPlagas):
                    productos_serializados.append({
                        "nombre": p.nombre,
                        "precio": p.precio,
                        "registro_ica": p.registro_ica,
                        "frecuencia_aplicacion": p.frecuencia_aplicacion,
                        "periodo_carencia": p.periodo_carencia,
                        "tipo": "Control Plagas"
                    })
                elif isinstance(p, ControlFertilizantes):
                    productos_serializados.append({
                        "nombre": p.nombre,
                        "precio": p.precio,
                        "registro_ica": p.registro_ica,
                        "frecuencia_aplicacion": p.frecuencia_aplicacion,
                        "fecha_ultima_aplicacion": p.fecha_ultima_aplicacion,
                        "tipo": "Fertilizante"
                    })
                elif isinstance(p, Antibiotico):
                    productos_serializados.append({
                        "nombre": p.nombre,
                        "precio": p.precio,
                        "dosis": p.dosis,
                        "tipo_animal": p.tipo_animal,
                        "tipo": "Antibiotico"
                    })
            facturas_serializadas.append({
                "cliente": factura.cliente.cedula,
                "productos": productos_serializados,
                "total": factura.total
            })
        json.dump(facturas_serializadas, file, indent=4)
    
    #Guardamos los productos
    with open(PRODUCTOS_FILE, "w") as file:
        productos_serializados = []
        for producto in productos:
            if isinstance(producto, ControlPlagas):
                productos_serializados.append({
                    "nombre": producto.nombre,
                    "precio": producto.precio,
                    "registro_ica": producto.registro_ica,
                    "frecuencia_aplicacion": producto.frecuencia_aplicacion,
                    "periodo_carencia": producto.periodo_carencia,
                    "tipo": "Control Plagas"
                })
            elif isinstance(producto, ControlFertilizantes):
                productos_serializados.append({
                    "nombre": producto.nombre,
                    "precio": producto.precio,
                    "registro_ica": producto.registro_ica,
                    "frecuencia_aplicacion": producto.frecuencia_aplicacion,
                    "fecha_ultima_aplicacion": producto.fecha_ultima_aplicacion,
                    "tipo": "Fertilizante"
                })
            elif isinstance(producto, Antibiotico):
                productos_serializados.append({
                    "nombre": producto.nombre,
                    "precio": producto.precio,
                    "dosis": producto.dosis,
                    "tipo_animal": producto.tipo_animal,
                    "tipo": "Antibiotico"
                })
        
        json.dump(productos_serializados, file, indent=4)


def cargar_datos():
    global clientes, facturas, productos
    
    #Cargamos los clientes
    if os.path.exists(CLIENTES_FILE):
        with open(CLIENTES_FILE, "r") as file:
            datos_clientes = json.load(file)
            clientes = {cedula: Cliente(data["nombre"], data["cedula"]) 
                        for cedula, data in datos_clientes.items()}
    
    #Cargamos las facturas con sus respectivos precios y productos
    if os.path.exists(FACTURAS_FILE):
        with open(FACTURAS_FILE, "r") as file:
            datos_facturas = json.load(file)
            for data in datos_facturas:
                cliente = clientes.get(data["cliente"])
                if cliente:
                    factura = Factura(cliente)
                    for p in data["productos"]:
                        producto = None
                        tipo = p.get("tipo")
                        if tipo == "Control Plagas":
                            producto = ControlPlagas(
                                p["nombre"],
                                p["precio"],
                                p["registro_ica"],
                                p["frecuencia_aplicacion"],
                                p["periodo_carencia"]
                            )
                        elif tipo == "Fertilizante":
                            producto = ControlFertilizantes(
                                p["nombre"],
                                p["precio"],
                                p["registro_ica"],
                                p["frecuencia_aplicacion"],
                                p["fecha_ultima_aplicacion"]
                            )
                        elif tipo == "Antibiotico":
                            producto = Antibiotico(
                                p["nombre"],
                                p["precio"],
                                p["dosis"],
                                p["tipo_animal"]
                            )
                        else:
                            print(f"Advertencia: Tipo de producto '{tipo}' desconocido.")
                        if producto:
                            factura.agregar_producto(producto)
                    facturas.append(factura)
    
    #Cargamos los productos
    if os.path.exists(PRODUCTOS_FILE):
        with open(PRODUCTOS_FILE, "r") as file:
            datos_productos = json.load(file)
            productos = []
            for p in datos_productos:
                producto = None
                tipo = p.get("tipo")
                if tipo == "Control Plagas":
                    producto = ControlPlagas(
                        p["nombre"],
                        p["precio"],
                        p["registro_ica"],
                        p["frecuencia_aplicacion"],
                        p["periodo_carencia"]
                    )
                elif tipo == "Fertilizante":
                    producto = ControlFertilizantes(
                        p["nombre"],
                        p["precio"],
                        p["registro_ica"],
                        p["frecuencia_aplicacion"],
                        p["fecha_ultima_aplicacion"]
                    )
                elif tipo == "Antibiotico":
                    producto = Antibiotico(
                        p["nombre"],
                        p["precio"],
                        p["dosis"],
                        p["tipo_animal"]
                    )
                else:
                    print(f"Advertencia: Tipo de producto '{tipo}' desconocido.")
                if producto:
                    productos.append(producto)



#Creamos la funcion que registra el cliente y revisa a su vez la base de datos para comprobar que no se repite la cedula
def registrar_cliente():
    def guardar_cliente():
        nombre = entry_nombre.get()
        cedula = entry_cedula.get()
        if cedula in clientes:
            messagebox.showerror("Error", "Este cliente ya está registrado.")
        else:
            clientes[cedula] = Cliente(nombre, cedula)
            messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente.")
            ventana.destroy()

    ventana = tk.Toplevel()
    ventana.title("Registrar Cliente")
    ventana.geometry("400x250")
    
    tk.Label(ventana, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()
    
    tk.Label(ventana, text="Cédula:").pack()
    entry_cedula = tk.Entry(ventana)
    entry_cedula.pack()
    
    tk.Button(ventana, text="Registrar", command=guardar_cliente).pack()

#Funcion para visualizar los clientes del archivo JSON
def ver_clientes():
    ventana = tk.Toplevel()
    ventana.title("Clientes Registrados")
    ventana.geometry("400x400")
    
    texto = tk.Text(ventana)
    texto.pack()
    
    if not clientes:
        texto.insert(tk.END, "No hay clientes registrados.")
    else:
        for cedula, cliente in clientes.items():
            texto.insert(tk.END, f"Nombre: {cliente.nombre}, Cédula: {cedula}\n")

#Funcion para visualizar los productos registrado por el cliente en el archivo JSON
def ver_productos():
    ventana = tk.Toplevel()
    ventana.title("Productos Disponibles")
    ventana.geometry("500x500")
    
    texto = tk.Text(ventana)
    texto.pack(fill="both", expand=True)
    
    if not productos:
        texto.insert(tk.END, "No hay productos registrados.")
    else:
        productos_mostrados = set()  #Evitamos que se dupliquen los productos
                                     #Asi el usuario puede comprar 8 unidades de un producto sin que le aparezca 8 veces el mismo producto con las mismas caracteristicas 
        
        for producto in productos:
            if producto.nombre in productos_mostrados:
                continue 
            
            productos_mostrados.add(producto.nombre)
            
            texto.insert(tk.END, f"Nombre: {producto.nombre}\n")
            texto.insert(tk.END, f"Precio: ${producto.precio:.2f}\n")
            
            if isinstance(producto, ControlPlagas):
                texto.insert(tk.END, "Tipo: Control de Plagas\n")
                texto.insert(tk.END, f"Registro ICA: {producto.registro_ica}\n")
                texto.insert(tk.END, f"Frecuencia de Aplicación: {producto.frecuencia_aplicacion}\n")
                texto.insert(tk.END, f"Periodo de Carencia: {producto.periodo_carencia}\n")
            elif isinstance(producto, ControlFertilizantes):
                texto.insert(tk.END, "Tipo: Fertilizante\n")
                texto.insert(tk.END, f"Registro ICA: {producto.registro_ica}\n")
                texto.insert(tk.END, f"Frecuencia de Aplicación: {producto.frecuencia_aplicacion}\n")
                texto.insert(tk.END, f"Fecha Última Aplicación: {producto.fecha_ultima_aplicacion}\n")
            elif isinstance(producto, Antibiotico):
                texto.insert(tk.END, "Tipo: Antibiotico\n")
                texto.insert(tk.END, f"Dosis: {producto.dosis} mg\n")
                texto.insert(tk.END, f"Tipo de Animal: {producto.tipo_animal}\n")
            
            texto.insert(tk.END, "-"*40 + "\n\n")


#Funcion para visualizar las facturas del archivo JSON
def ver_facturas():
    ventana = tk.Toplevel()
    ventana.title("Facturas Registradas")
    ventana.geometry("600x500")
    
    texto = tk.Text(ventana)
    texto.pack()
    
    if not facturas:
        texto.insert(tk.END, "No hay facturas registradas.")
    else:
        for i, factura in enumerate(facturas, 1):
            texto.insert(tk.END, f"Factura {i}: \n")
            texto.insert(tk.END, f"Cédula del Cliente: {factura.cliente.cedula}\n")
            texto.insert(tk.END, f"Nombre del Cliente: {factura.cliente.nombre}\n")
            for producto in factura.productos:
                texto.insert(tk.END, f"  - {producto.nombre}: ${producto.precio:.2f}\n")
            texto.insert(tk.END, f"Total: ${factura.total:.2f}\n\n")


def crear_factura():
    global factura_actual
    factura_actual = None

    #La ventana para la factura
    ventana = tk.Toplevel()
    ventana.title("Crear Factura")
    ventana.geometry("500x400")
    ventana.grab_set()

    #Funcion para poder ver todos los campos necesarios para cada tipo de producto
    def mostrar_campos_adicionales():
        for widget in ventana.winfo_children():
            widget.destroy()

        #Campos basicos de cada producto
        tk.Label(ventana, text="Nombre del Producto:").pack()
        entry_producto = tk.Entry(ventana)
        entry_producto.pack()

        tk.Label(ventana, text="Precio del Producto:").pack()
        entry_precio = tk.Entry(ventana)
        entry_precio.pack()

        tk.Label(ventana, text="Registro ICA:").pack()
        entry_ica = tk.Entry(ventana)
        entry_ica.pack()

        
        tipo_producto = tipo_var.get()

        #Campos según el tipo de producto
        if tipo_producto == "Control Plagas":
            tk.Label(ventana, text="Frecuencia de Aplicación (días):").pack()
            entry_frecuencia_aplicacion = tk.Entry(ventana)
            entry_frecuencia_aplicacion.pack()

            tk.Label(ventana, text="Periodo de Carencia (días):").pack()
            entry_periodo_carencia = tk.Entry(ventana)
            entry_periodo_carencia.pack()

        elif tipo_producto == "Fertilizante":
            tk.Label(ventana, text="Frecuencia de Aplicación (días):").pack()
            entry_frecuencia_aplicacion = tk.Entry(ventana)
            entry_frecuencia_aplicacion.pack()

            tk.Label(ventana, text="Fecha Última Aplicación:").pack()
            entry_fecha_ultima_aplicacion = tk.Entry(ventana)
            entry_fecha_ultima_aplicacion.pack()

        elif tipo_producto == "Antibiotico":
            tk.Label(ventana, text="Dosis (mg):").pack()
            entry_dosis = tk.Entry(ventana)
            entry_dosis.pack()

            tk.Label(ventana, text="Tipo de Animal (Bovino, Caprino, Porcino):").pack()
            entry_tipo_animal = tk.Entry(ventana)
            entry_tipo_animal.pack()

        #Funcion para agregar los productos a la factura
        def agregar_producto():
            if factura_actual is None:
                messagebox.showerror("Error", "Debe seleccionar un cliente antes de agregar productos.")
                return

            nombre_producto = entry_producto.get()
            try:
                precio = float(entry_precio.get())
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido.")
                return
            registro_ica = entry_ica.get()

            if tipo_producto == "Control Plagas":
                frecuencia_aplicacion = entry_frecuencia_aplicacion.get()
                periodo_carencia = entry_periodo_carencia.get()
                if not (frecuencia_aplicacion.isdigit() and periodo_carencia.isdigit()):
                    messagebox.showerror("Error", "La frecuencia y el periodo deben ser números válidos.")
                    return
                producto = ControlPlagas(
                    nombre_producto, precio, registro_ica, int(frecuencia_aplicacion), int(periodo_carencia)
                )

            elif tipo_producto == "Fertilizante":
                frecuencia_aplicacion = entry_frecuencia_aplicacion.get()
                fecha_ultima_aplicacion = entry_fecha_ultima_aplicacion.get()
                if not frecuencia_aplicacion.isdigit():
                    messagebox.showerror("Error", "La frecuencia debe ser un número válido.")
                    return
                producto = ControlFertilizantes(
                    nombre_producto, precio, registro_ica, int(frecuencia_aplicacion), fecha_ultima_aplicacion
                )

            elif tipo_producto == "Antibiotico":
                dosis = entry_dosis.get()
                tipo_animal = entry_tipo_animal.get()
                if not dosis.isdigit():
                    messagebox.showerror("Error", "La dosis debe ser un número válido.")
                    return
                producto = Antibiotico(
                    nombre_producto, precio, int(dosis), tipo_animal
                )

            factura_actual.agregar_producto(producto)
            productos.append(producto)
            messagebox.showinfo("Éxito", f"Producto {nombre_producto} agregado a la factura.")

        #Funcion para finalizar y guardar
        def finalizar_factura():
            if factura_actual is None:
                messagebox.showerror("Error", "No se ha creado una factura válida.")
                return
            facturas.append(factura_actual)
            messagebox.showinfo("Factura", f"Factura creada con total: ${factura_actual.total:.2f}")
            ventana.destroy()

        #Botones de agregar y finalizar
        tk.Button(ventana, text="Agregar Producto", command=agregar_producto).pack()
        tk.Button(ventana, text="Finalizar Factura", command=finalizar_factura).pack()

    #Función para comprobar si el cliente con XxXx cedula existe
    def buscar_cliente():
        global factura_actual
        cedula = entry_cedula.get()
        if cedula in clientes:
            factura_actual = Factura(clientes[cedula])
            messagebox.showinfo("Cliente", f"Cliente {clientes[cedula].nombre} seleccionado.")
            mostrar_campos_adicionales()
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")

    tk.Label(ventana, text="Cédula del Cliente:").pack()
    entry_cedula = tk.Entry(ventana)
    entry_cedula.pack()

    tk.Button(ventana, text="Buscar Cliente", command=buscar_cliente).pack()

    tk.Label(ventana, text="Tipo de Producto:").pack()
    tipo_var = tk.StringVar(value="Control Plagas")
    tk.OptionMenu(ventana, tipo_var, "Control Plagas", "Fertilizante", "Antibiotico").pack()

    guardar_datos()


    
def salir():
    guardar_datos()
    root.quit()

cargar_datos()

#Ventana principal - Menu
root = tk.Tk()
root.title("Sistema de Facturación")
root.geometry("600x500")
root.grab_set()

tk.Label(root, text="Sistema de Facturación", font=("Arial", 16, "bold")).pack(pady=20)

tk.Button(root, text="Registrar Cliente", command=registrar_cliente, width=30, height=2).pack(pady=5)
tk.Button(root, text="Crear Factura", command=crear_factura, width=30, height=2).pack(pady=5)
tk.Button(root, text="Ver Clientes", command=ver_clientes, width=30, height=2).pack(pady=5)
tk.Button(root, text="Ver Productos", command=ver_productos, width=30, height=2).pack(pady=5)
tk.Button(root, text="Ver Facturas", command=ver_facturas, width=30, height=2).pack(pady=5)
tk.Button(root, text="Salir", command=salir, width=30, height=2, bg="red", fg="white").pack(pady=20)

root.mainloop()
