import tkinter as tk
import re
import Personas_Datos as crud 
from tkinter import ttk
from tkinter import messagebox

# Ventana 

ventana= tk.Tk()

ventana.title("Aplicacion con BD sql lite")

alto=600
ancho=950

# Centrar la ventana de acuerdo con el tamaño de la pantalla
x_v=ventana.winfo_screenwidth() // 2 - ancho // 2  
x_y=ventana.winfo_screenheight() // 2 - alto // 2

pos=str(ancho)+"x"+str(alto)+"+"+str(x_v)+"+"+str(x_y)
ventana.geometry(pos)

ventana.resizable(0,0)
ventana.state("zoomed")
ventana.config(bg="#fff")

## VARIABLES

txt_id = tk.StringVar()
txt_dni = tk.StringVar()
txt_edad = tk.StringVar()
txt_nombre = tk.StringVar()
txt_apellido = tk.StringVar()
txt_direccion = tk.StringVar()
txt_correo = tk.StringVar()

## FUNCIONES

def creditos():
  messagebox.showinfo("Créditos",
                      """ Creado por : Santiago Agudelo
                      ------------------------------------
                      GitHub: https://github.com/TIAGSA
                      """)
 
def salir():
  res=messagebox.askquestion("Salir","¿Desea salir de la aplicacion?")
  if res == "yes":
   ventana.destroy()   

def datosTabla():
  tabla.delete(*tabla.get_children())
  res= crud.findAll()
  personas=res.get("Total_personas")
  for fila in personas:
    row=list(fila)
    row.pop(0)
    row=tuple(row)
    tabla.insert("",tk.END,text=id,values=row)

def limpiarCampos():
 txt_dni.set("")
 txt_nombre.set("")
 txt_apellido.set("")
 txt_edad.set("")
 txt_correo.set("")
 txt_direccion.set("")
    

def guardar():
 try:
  per={}
  error= False
  if txt_dni.get().isnumeric():
     per['dni']=int(txt_dni.get())
  else:
   txt_dni.set("")
   e_dni.focus()
   messagebox.showerror("ERROR","El dni debe ser numero")
   error=True
  per['nombre']=txt_nombre.get()
  per['apellido']=txt_apellido.get()
  per['direccion']=txt_direccion.get()
  if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',txt_correo.get()):
    per['correo']=txt_correo.get()
  else:
   messagebox.showerror("ERROR","Porfavor introduzca un correo valido")
   txt_correo.set("")
   e_correo.focus()
   error=True
  if txt_edad.get().isnumeric():
   per['edad']=int(txt_edad.get())
  else:
    txt_edad.set("")
    e_edad.focus()
    messagebox.showerror("ERROR","La edad debe ser un numero")
    error=True
  if not error:
   res=crud.save(per)
   if res.get('Respuesta'):
    datosTabla()
    messagebox.showinfo("Mensaje",res.get('Mensaje')) 
   else:
    messagebox.showinfo("Mensaje",res.get('Mensaje'))  
 except Exception as ex:
   messagebox.showerror("ERROR", f"Ocurrió un error inesperado: {str(ex)}")

def consulta():
 if txt_dni.get()!="":
  tabla.delete(*tabla.get_children())
  dni=int(txt_dni.get())
  res=crud.find(dni)
  if res.get('Respuesta'):
    per=res.get('Persona')
    del per['Id']
    values=tuple(per.values())
    tabla.insert("",tk.END,values=values)
    txt_dni.set(per.get('Dni'))
    txt_nombre.set(per.get('Nombre'))
    txt_apellido.set(per.get('Apellido')) 
    txt_edad.set(per.get('Edad')) 
    txt_correo.set(per.get('Correo')) 
    txt_direccion.set(per.get('Direccion')) 
  else:
   e_dni.focus()
   messagebox.showerror("Mensaje",res.get('Mensaje'))
   limpiarCampos()
 else: 
  e_dni.focus()
  messagebox.showerror("Mensaje","No puede estar vacio el campo de DNI") 
  limpiarCampos()

def actualizar():
 per_up={'dni':int(txt_dni.get()),'edad':int(txt_edad.get()),'nombre':txt_nombre.get(),'apellido':txt_apellido.get(),'direccion':txt_direccion.get(),'correo':txt_correo.get()}
 res=crud.update(per_up)
 if res.get('respuesta'):
  messagebox.showinfo("OK",res.get('mensaje')) 
  limpiarCampos()
  datosTabla()
 else:
  messagebox.showerror("ERROR",res.get('mensaje'))

def eliminar():
 if txt_dni.get()!="":
  res=crud.find(txt_dni.get())
  if res.get('Respuesta'):
   per=res.get("Persona")
   respuesta=messagebox.askquestion("Confirmar",f'¿Desea eliminar a {per.get("Nombre")} {per.get("Apellido")} con el DNI {per.get("Dni")}')
   if respuesta =="yes":
    res=crud.delete(per.get("Id"))
    if res.get('respuesta'):
     datosTabla() 
     limpiarCampos()
     messagebox.showinfo("OK",res.get('mensaje'))
    else:
     messagebox.showerror("ERROR","No se logro eliminar la persona"+res.get('mensaje'))
  else:
   messagebox.showerror("Mensaje","El campo del dni no puede ir vacio")
 
## FIN FUNCIONES

## GUI

Fuente=("Monserat",12)
tk.Label(ventana,text="DNI :",anchor="w",justify="left",width=10,font=Fuente,bg="#CCFFFF").grid(row=0,column=0,padx=10,pady=8)
tk.Label(ventana,text="Nombre :",anchor="w",justify="left",width=10,font=Fuente,bg="#fff").grid(row=1,column=0,padx=10,pady=8)
tk.Label(ventana,text="Apellido :",anchor="w",justify="left",width=10,font=Fuente,bg="#fff").grid(row=2,column=0,padx=10,pady=8)
tk.Label(ventana,text="Direccion :",anchor="w",justify="left",width=10,font=Fuente,bg="#fff").grid(row=3,column=0,padx=10,pady=8)
tk.Label(ventana,text="Correo :",anchor="w",justify="left",width=10,font=Fuente,bg="#fff").grid(row=4,column=0,padx=10,pady=8)
tk.Label(ventana,text="Edad :",anchor="w",justify="left",width=10,font=Fuente,bg="#fff").grid(row=5,column=0,padx=10,pady=8)

#Inputs

e_dni=ttk.Entry(ventana,font=Fuente,textvariable=txt_dni)
e_nombre=ttk.Entry(ventana,font=Fuente,textvariable=txt_nombre)
e_apellido=ttk.Entry(ventana,font=Fuente,textvariable=txt_apellido)
e_direccion=ttk.Entry(ventana,font=Fuente,textvariable=txt_direccion)
e_correo=ttk.Entry(ventana,font=Fuente,textvariable=txt_correo)
e_edad=ttk.Entry(ventana,font=Fuente,textvariable=txt_edad)
e_dni.focus()

e_dni.grid(row=0,column=1)
e_nombre.grid(row=1,column=1)
e_apellido.grid(row=2,column=1)
e_direccion.grid(row=3,column=1)
e_correo.grid(row=4,column=1)
e_edad.grid(row=5,column=1)

#Botones

iconNew=tk.PhotoImage(file="assets/IconNEW.png")
iconFind=tk.PhotoImage(file="assets/IconFIND.png")
iconUpdate=tk.PhotoImage(file="assets/IconUpdate.png")
iconDelete=tk.PhotoImage(file="assets/IconDelete.png")


btn_save=ttk.Button(ventana,text="Guardar",command=guardar,image=iconNew,compound="left")
btn_find=ttk.Button(ventana,text="Consultar",command=consulta,image=iconFind,compound="left")
btn_update=ttk.Button(ventana,text="Actualizar",command=actualizar,image=iconUpdate,compound="left")
btn_delete=ttk.Button(ventana,text="Eliminar",command=eliminar,image=iconDelete,compound="left")

btn_save.place(x=10,y=280)
btn_find.place(x=120,y=280)
btn_update.place(x=230,y=280)
btn_delete.place(x=340,y=280)


titulo=tk.Label(ventana,text="LISTA DE PERSONAS",font=("Arial",15),bg="#fff").place(x=600,y=10)

tabla=ttk.Treeview(ventana)

tabla.place(x=450,y=40)

tabla["columns"]=("DNI","EDAD","NOMBRE","APELLIDO","DIRECCION","CORREO")
tabla.column("#0",width=0,stretch="NO")
tabla.column("DNI",width=100,anchor="center")
tabla.column("EDAD",width=100,anchor="center")
tabla.column("NOMBRE",width=150,anchor="center")
tabla.column("APELLIDO",width=150,anchor="center")
tabla.column("DIRECCION",width=170,anchor="center")
tabla.column("CORREO",width=160,anchor="center")

tabla.heading("#0",text="")
tabla.heading("DNI",text="DNI")
tabla.heading("EDAD",text="Edad")
tabla.heading("NOMBRE",text="Nombre")
tabla.heading("APELLIDO",text="Apellido")
tabla.heading("DIRECCION",text="Dirección")
tabla.heading("CORREO",text="Correo")


# MENU

menuTop=tk.Menu(ventana)

m_archivo= tk.Menu(menuTop,tearoff=0)
m_archivo.add_command(label="Créditos",command=creditos)
m_archivo.add_command(label="Salir",command=salir)
menuTop.add_cascade(label="Archivo",menu=m_archivo)


m_limpiar= tk.Menu(menuTop,tearoff=0)
m_limpiar.add_command(label="Limpiar campos",command=limpiarCampos)
menuTop.add_cascade(label="Limpiar",menu=m_limpiar)

m_crud= tk.Menu(menuTop,tearoff=0)
m_crud.add_command(label="Guardar",command=guardar)
m_crud.add_command(label="Consultar",command=consulta)
m_crud.add_command(label="Consultar-Todos",command=datosTabla)
m_crud.add_command(label="Actualizar",command=actualizar)
m_crud.add_command(label="Eliminar",command=eliminar)
menuTop.add_cascade(label="CRUD",menu=m_crud)

ventana.config(menu=menuTop)



ventana.mainloop()
