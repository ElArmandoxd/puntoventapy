from appJar import gui
import sqlite3

def salir():
    app.stop()

def guardar():
    print("Nuevo producto: \n")
    producto = app.getEntry("producto")
    print("\t" + producto + "\n")
    precio = app.getEntry("precio")
    print("\t" + precio + "\n")
    tipo = app.getEntry("tipo")
    print("\t" + tipo + "\n")
    cantidad = app.getEntry("cantidad")
    print("\t" + cantidad + "\n")
    
    conn = sqlite3.connect("almacen.db")
    cursor_almacen = conn.cursor()

    tabla = """CREATE TABLE IF NOT EXISTS almacen(
        producto TEXT NOT NULL,
        precio TEXT NOT NULL,
        tipo TEXT NOT NULL,
        cantidad TEXT NOT NULL
    );"""
    cursor_almacen.execute(tabla)
    reg = (producto, precio, tipo, cantidad)
    cursor_almacen.execute("INSERT INTO almacen VALUES(?,?,?,?)", reg)
    conn.commit()
    conn.close()
    app.refreshDbTable("tabladb")

with gui("Punto de venta") as app:
    with app.tabbedFrame("Address Book"):
        with app.tab('Productos'):
            
            app.addLabel("titulo_ver", "Ver productos")
            app.addDbTable("tabladb", "almacen.db", "almacen")

        with app.tab('Añadir'):
            
            app.addLabel("almacen","Añadir producto")
            app.setLabelBg("almacen", "cyan")
            app.setLabelFg("almacen", "Black")
            app.setFont("almacen", 25)

            app.addLabelEntry("producto", label = "Nombre: ")
            app.addLabelEntry("precio", label = "Precio: ")
            app.addLabelEntry("tipo", label = "Tipo de producto: ")
            app.addLabelEntry("cantidad", label = "Cantidad: ")

            app.addButton("Guardar", guardar)
            app.addButton("Salir..", salir)
       
        with app.tab('Venta'):

            app.addLabel("Venta","Venta productos")
            app.addLabel("titulo_venta", "Vender productos")
            app.addDbTable("tablaventa", "almacen.db", "almacen")
            app.addButton("Salir...", salir)
            
