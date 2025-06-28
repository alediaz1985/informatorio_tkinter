from PIL import Image, ImageTk
import tkinter as tk
import time
from datetime import datetime


# este es un Diccionario de productos con los precios
productos_precios = {
    "Agua Mineral Barata": 550,
    "Coca-Cola": 3000,
    "Jugo Baggio 1L": 1399,
    "Surtidos": 1870,
    "Oreo": 2200,
    "Pepitos": 1600,
    "Chicle globo": 100,
    "Chocolate Barra": 1800,
    "Caramelos x10": 500
}


# ------- SPLASH SCREEN -------
splash = tk.Tk()
splash.overrideredirect(True)  # Quita barra de título
splash.geometry("400x300+500+200")  # Tamaño y posición

# Imagen del logo
imagen = Image.open("logo_inicio.png")  # Cambia por el nombre real de tu archivo
imagen = imagen.resize((400, 300))
imagen_tk = ImageTk.PhotoImage(imagen)
label_imagen = tk.Label(splash, image=imagen_tk)
label_imagen.pack()

# Mostrar splash 2 segundos y luego cerrar
splash.after(2000, splash.destroy)
splash.mainloop()

# Inicia la ventana del programa el tamaño de pantalla que va a tener
ventana = tk.Tk()
ventana.title("Kiosco de Alejandro")
ventana.geometry("900x650")

total_var = tk.StringVar()
total_var.set("Total: $0")

# primero definimos las funciones necesarias para el programa
def actualizar_hora():
    hora_actual = time.strftime('%H:%M:%S')
    reloj.config(text=hora_actual)
    ventana.after(1000, actualizar_hora)

def agregar_producto(nombre_producto):
    carrito.insert(tk.END, nombre_producto)
    total_var.set(calcular_total())

def eliminar_producto():
    seleccion = carrito.curselection()
    if seleccion:
        carrito.delete(seleccion)
        total_var.set(calcular_total())

def calcular_total():
    total = 0
    for i in carrito.get(0, tk.END):
        total += productos_precios.get(i, 0)
    return f"Total: ${total}"

def generar_comprobante():
    cliente = entry_cliente.get()
    if not cliente:
        cliente = "Capibara"
    hora = time.strftime('%H:%M:%S')
    fecha = time.strftime('%d/%m/%Y')
    productos = carrito.get(0, tk.END)
    total = calcular_total()

    comprobante = f"Kiosco de Alejandro - Comprobante de Compra\nCliente: {cliente}\nFecha: {fecha} - Hora: {hora}\n\nProductos:\n"
    for producto in productos:
        precio = productos_precios.get(producto, 0)
        comprobante += f"- {producto}: ${precio}\n"
    comprobante += f"\n{total}\n\n¡Gracias por su compra en el Informatorio!"

    # Sirve para mostrar el comprobante en una ventana emergente
    ventana_comprobante = tk.Toplevel(ventana)
    ventana_comprobante.title("Comprobante de compra de Informatorio")
    tk.Label(ventana_comprobante, text=comprobante, justify="left", padx=10, pady=10).pack()

    # Guardar historial
    with open("historial_compras.txt", "a", encoding="utf-8") as f:
        f.write(comprobante + "\n" + "-"*40 + "\n")

# Estado actual del tema
modo_oscuro_activado = False

# Función para alternar entre modo claro y oscuro
def alternar_modo():
    global modo_oscuro_activado
    if not modo_oscuro_activado:
        # Modo oscuro
        ventana.config(bg="#2e2e2e")
        reloj.config(bg="#2e2e2e", fg="white")
        entry_cliente.config(bg="black", fg="white", insertbackground="white")
        etiqueta_cliente.config(bg="#2e2e2e", fg="white")
        etiqueta_total.config(bg="#2e2e2e", fg="white")
        boton_comprobante.config(bg="#444", fg="white")
        boton_eliminar.config(bg="#444", fg="white")
        carrito.config(bg="black", fg="white")
        tema_menu.entryconfig(0, label="Modo Claro")
        modo_oscuro_activado = True
    else:
        # Modo claro
        ventana.config(bg="SystemButtonFace")
        reloj.config(bg="SystemButtonFace", fg="blue")
        entry_cliente.config(bg="white", fg="black", insertbackground="black")
        etiqueta_cliente.config(bg="SystemButtonFace", fg="black")
        etiqueta_total.config(bg="SystemButtonFace", fg="black")
        boton_comprobante.config(bg="SystemButtonFace", fg="black")
        boton_eliminar.config(bg="SystemButtonFace", fg="black")
        carrito.config(bg="white", fg="black")
        tema_menu.entryconfig(0, label="Modo Oscuro")
        modo_oscuro_activado = False


# Reloj
reloj = tk.Label(ventana, font=("Arial", 18), fg="blue")
reloj.pack(pady=5)
actualizar_hora()

# Entrada de cliente
etiqueta_cliente = tk.Label(ventana, text="Cliente: ")
etiqueta_cliente.pack()
entry_cliente = tk.Entry(ventana)
entry_cliente.pack(pady=5)

# Menú
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_productos = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Productos", menu=menu_productos)

# Submenús
bebidas = tk.Menu(menu_productos, tearoff=0)
galletitas = tk.Menu(menu_productos, tearoff=0)
golosinas = tk.Menu(menu_productos, tearoff=0)

menu_productos.add_cascade(label="Bebidas", menu=bebidas)
menu_productos.add_cascade(label="Galletitas", menu=galletitas)
menu_productos.add_cascade(label="Golosinas", menu=golosinas)

tema_menu = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Tema", menu=tema_menu)
tema_menu.add_command(label="Modo Oscuro", command=alternar_modo)

# Agregar productos con precios
for producto in ["Agua Mineral Barata", "Coca-Cola", "Jugo Baggio 1L"]:
    bebidas.add_command(label=f"{producto} - ${productos_precios[producto]}", command=lambda p=producto: agregar_producto(p))
for producto in ["Surtidos", "Oreo", "Pepitos"]:
    galletitas.add_command(label=f"{producto} - ${productos_precios[producto]}", command=lambda p=producto: agregar_producto(p))
for producto in ["Chicle globo", "Chocolate Barra", "Caramelos x10"]:
    golosinas.add_command(label=f"{producto} - ${productos_precios[producto]}", command=lambda p=producto: agregar_producto(p))

# Carrito lista de productos 10 y luego se activa el scroll
frame_carrito = tk.Frame(ventana)
frame_carrito.pack(pady=10)

scrollbar = tk.Scrollbar(frame_carrito)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

carrito = tk.Listbox(frame_carrito, yscrollcommand=scrollbar.set, width=50, height=10)
carrito.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=carrito.yview)

# Total de compra 
total_var = tk.StringVar()
total_var.set("Total: $0")
etiqueta_total = tk.Label(ventana, textvariable=total_var, font=("Arial", 14))
etiqueta_total.pack(pady=5)

# Botón eliminar sirve para eliminar el producto seleccionado
boton_eliminar = tk.Button(ventana, text="Eliminar producto seleccionado", command=eliminar_producto)
boton_eliminar.pack(pady=5)

# Botón para generar el comprobante
boton_comprobante = tk.Button(ventana, text="Generar comprobante", command=generar_comprobante)
boton_comprobante.pack(pady=5)

# Incia el Programa de kiosco
ventana.mainloop()
