from appJar import gui
import sqlite3

def registrarVenta():
    producto_venta = app.getOptionBox("Productos")
    cantidad_venta = int(app.getEntry("cantidades"))
    indice = productos.index(producto_venta)
    restantes = int(cantidades[indice])
    if restantes >= cantidad_venta:
        precio_venta = float(precios[indice]) * cantidad_venta
        cantidad_restante = restantes - cantidad_venta
        app.addLabel("total", "Total: " + str(precio_venta))
        conn = sqlite3.connect("almacen.db")
        cursor_venta = conn.cursor()
        tabla_venta = """CREATE TABLE IF NOT EXISTS ventas(
            producto TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INT NOT NULL
        );"""
        cursor_venta.execute(tabla_venta)
        reg_venta = (producto_venta, precio_venta, cantidad_venta)
        cursor_venta.execute("INSERT INTO ventas VALUES(?,?,?)", reg_venta)
        cursor_venta.execute("UPDATE almacen SET cantidad = ? WHERE producto = ?",(cantidad_restante, producto_venta))
        conn.commit()
        conn.close()
        app.refreshDbTable("tabladb")
        app.refreshDbTable("tablaventas")
        app.infoBox("Exito","Venta exitosa")
    else:
        app.errorBox("No hay suficientes","No hay suficientes objetos en existencia, prueba con una cantidad menor")

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
    app.infoBox("Exito","Producto registrado")

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

            conn = sqlite3.connect("almacen.db")
            conn.row_factory = lambda cursor, row: row[0]
            cursor = conn.cursor()
            productos = cursor.execute('SELECT producto FROM almacen').fetchall()
            precios = cursor.execute('SELECT precio FROM almacen').fetchall()
            cantidades = cursor.execute('SELECT cantidad FROM almacen').fetchall()
            conn.close()
            app.addLabelOptionBox("Productos", productos)
            app.addLabelEntry("cantidades", label = "Cantidad: ")
            app.addButton("Vender", registrarVenta)

        with app.tab('Reporte venta'):
            app.addLabel("titulo_ver_reporte", "Ver reporte ventas")
            app.addDbTable("tablaventas", "almacen.db", "ventas")
    