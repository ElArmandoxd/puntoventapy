from appJar import gui

app = gui()

def guardar():
    print("Nuevo contacto: \n")
    nombre = app.getEntry("nombre")
    print("\t"+nombre + " el chido \n")
    paterno = app.getEntry("paterno")
    print("\t"+paterno + "\n")
    materno = app.getEntry("materno")
    print("\t"+materno + "\n")
    direccion = app.getEntry("direccion")
    print("\t"+direccion + "\n")
    telefono = app.getEntry("telefono")
    print("\t"+telefono + "\n")

    conn = sqlite3.connect("agenda.db")
    cursor_agenda = conn.cursor()

    tabla = """CREATE TABLE IF NOT EXISTS agenda(
        nombre TEXT NOT NULL,
        paterno TEXT NOT NULL,
        materno TEXT NOT NULL,
        direccion TEXT NOT NULL,
        telefono TEXT NOT NULL
    );"""
    cursor_agenda.execute(tabla)
    reg = (nombre, paterno, materno, direccion, telefono)
    cursor_agenda.execute("INSERT INTO agenda VALUES(?,?,?,?,?)", reg)
    conn.commit()

app.addLabel("Agenda", "Agenda")
app.setLabelBg("Agenda", "Blue")

app.addLabelEntry("nombre", label = "Nombre: ")
app.addLabelEntry("paterno", label = "Paterno: ")
app.addLabelEntry("materno", label = "Materno: ")
app.addLabelEntry("direccion", label = "Direccion: ")
app.addLabelEntry("telefono", label = "Telefono: ")

app.addButton("guardar", guardar)

app.go()