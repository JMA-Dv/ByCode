from tkinter import *
from tkinter import filedialog as FileDialog
from io import open
from tkinter import messagebox as mguardar
import Lexer

ruta = "" # La utilizaremos para almacenar la ruta del fichero

def nuevo():
    global ruta
    mensaje.set("Nuevo fichero")
    ruta = ""
    texto.delete(1.0, "end")
    root.title("Compilador Semántico")

def abrir():
    global ruta
    mensaje.set("Abrir fichero")
    ruta = FileDialog.askopenfilename(
        initialdir='.', 
        filetypes=(("Ficheros de texto", "*.txt"),),
        title="Abrir un fichero de texto")

    if ruta != "":
        fichero = open(ruta, 'r')
        contenido = fichero.read()
        texto.delete(1.0,'end')
        texto.insert('insert', contenido)
        fichero.close()
        root.title(ruta + " - Compilador Semántico")

def guardar():
    mensaje.set("Guardar fichero")
    if ruta != "":
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
        mguardar.showinfo("Información", "Los datos fueron guardados en el archivo.")
    else:
        guardar_como()

def guardar_como():
    global ruta
    mensaje.set("Guardar fichero como")

    fichero = FileDialog.asksaveasfile(title="Guardar En", 
        mode="w", defaultextension=".txt")

    if fichero is not None:
        ruta = fichero.name
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Guardar En ")
        mb.showinfo("Información", "Los datos fueron guardados en el archivo.")
    else:
        mensaje.set("Guardado cancelado")
        ruta = ""
#crea el metodo para copiar el ttexto del widgets texto pegarlo al widgets caja
def copiar():
    contenidos=texto.get(1.0,'end-1c')
    #caja.insert('insert',contenidos)
    code = texto.get(1.0,'end-1c')
    result,error = Lexer.run('<tests>',code.lstrip())
    if error:
        print(error.as_string())
        caja.insert('insert',error.as_string())
    else: 
        print(result)
        caja.insert('insert',result,'\n')


def eliminar():
     caja.delete (1.0, END)
  
# Configuración de la raíz
root = Tk()
root.title("Compilador Semántico")
root.resizable(False, False)
root.geometry("830x500")
root.config(bg="#2a7373")
# Menú superior
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
#se mandan a llamar los metodos command=nuevo
filemenu.add_command(label="Nuevo", command=nuevo)
filemenu.add_command(label="Abrir", command=abrir)
filemenu.add_command(label="Guardar", command=guardar)
filemenu.add_command(label="Guardar En", command=guardar_como)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(menu=filemenu, label="Archivo")

# Caja de texto central
#es donde va a r el codigo
texto = Text(root)
#este comando de .place es para poner la posicion de cada widget
texto.place(x = 10, y = 5)
#y el comando .config es el tamaño del widget
texto.config(height=12, width=90, font=("Consolas",12),selectbackground="red")

##crea el boton 
caja = Text(root)
caja.place(width=800,height=90,x = 10, y = 330)

#Entry(root,textvariable=r).place(x = 10, y = 330)
boton=Button(root,text="Limpiar", width=25,command=eliminar)
boton.pack() 
boton.place(x=450,y=280)

botoncpiar= Button(root, text='Veriicar Código', width=25,command=copiar) 
botoncpiar.pack() 
botoncpiar.place(x=640, y = 280)
#El label de la salida
Label(root, text="Salida").place(x=10,y=280)
         
# Monitor inferior
mensaje = StringVar()
mensaje.set("Bienvenido al Compilador Semántico")
monitor = Label(root, textvar=mensaje, justify='left')
monitor.place(x=350,y=450)

#El menu
root.config(menu=menubar)

root.mainloop()