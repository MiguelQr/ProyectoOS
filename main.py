from tkinter import *
from tkinter import ttk
from grafico import GraficoMemoria

#Diccionario de la tabla de procesos
data = {'A':[8,1,7,0],
        'B':[14,2,7,0],
        'C':[18,3,4,0],
        'D':[6,4,6,0],
        'E':[14,5,5,0]
}

#Grafico de memoria
#Inicializar con datos, tamaño del OS, tamaño de memoria restante
gm = GraficoMemoria(data,10, 54)

paso = 0

#Callback del boton para cada paso
def siguientePaso():
    global paso
    paso += 1

    btn_text.set("Paso "+str(paso))

    #Borrar las tablas
    tp.delete(*tp.get_children())
    count_tp = 1

    tal.delete(*tal.get_children())
    count_tal = 1
    
    #Obtener listas de los espacios de memoria
    memoria = gm.siguiente_paso(paso)

    for espacio in memoria:
        #Si hay un proceso
        if espacio[0]:
            tp.insert(parent='', index=count_tp, iid=count_tp, text='', values=(count_tp,espacio[1], espacio[3],'Ocupado',espacio[4]))
            count_tp +=1
        #Si es area libre
        else:
            tal.insert(parent='', index=count_tal, iid=count_tal, text='', values=(count_tal,espacio[1],espacio[3],'Libre'))
            count_tal +=1

root = Tk()

root.title("Proyecto SO")
root.geometry("1000x500")

label0 = Label(text="SIMULACIÓN DE ASIGNACIÓN DE MEMORIA CON MVT")
label0.grid(column=1,row=0)

#Tabla de procesos
proc = ttk.Treeview(root, height=5)
proc['columns'] = ('Proceso', 'Tamano', 'Tiempo', 'Duracion')
proc.column("#0", width=0, stretch=False)
proc.column("Proceso", anchor=CENTER, width=80, stretch=False)
proc.column("Tamano", anchor=CENTER, width=80, stretch=False)
proc.column("Tiempo", anchor=CENTER, width=80, stretch=False)
proc.column("Duracion", anchor=CENTER, width=80, stretch=False)

proc.heading('#0', text='', anchor=CENTER)
proc.heading('Proceso', text='Proceso', anchor=CENTER)
proc.heading('Tamano', text='Tamaño', anchor=CENTER)
proc.heading('Tiempo', text='Tiempo de Llegada', anchor=CENTER)
proc.heading('Duracion', text='Duración (Tiempo en que se finaliza)', anchor=CENTER)

proc.insert(parent='', index=0, iid=0, text='', values=('A','8K','1','7'))
proc.insert(parent='', index=1, iid=1, text='', values=('B','14K','2','7'))
proc.insert(parent='', index=2, iid=2, text='', values=('C','18K','3','4'))
proc.insert(parent='', index=3, iid=3, text='', values=('D','6K','4','6'))
proc.insert(parent='', index=4, iid=4, text='', values=('E','14K','5','5'))

proc.grid(column=1,row=1)

label1 = Label(text="Tabla Áreas Libres (TAL[])")
label1.grid(column=0,row=2)

#Tabla de areas libres
tal = ttk.Treeview(root, height=5)
tal['columns'] = ('No', 'Localidad', 'Tamano', 'Estado')
tal.column("#0", width=0, stretch=False)
tal.column("No", anchor=CENTER, width=80, stretch=False)
tal.column("Localidad", anchor=CENTER, width=80, stretch=False)
tal.column("Tamano", anchor=CENTER, width=80, stretch=False)
tal.column("Estado", anchor=CENTER, width=80, stretch=False)

tal.heading('#0', text='', anchor=CENTER)
tal.heading('No', text='No', anchor=CENTER)
tal.heading('Localidad', text='Localidad', anchor=CENTER)
tal.heading('Tamano', text='Tamaño', anchor=CENTER)
tal.heading('Estado', text='Estado', anchor=CENTER)

espacios = gm.espacios[0]
tal.insert(parent='', index=1, iid=1, text='', values=(1,espacios[1],espacios[3],'Libre'))

tal.grid(column=0,row=3)

label2 = Label(text="Tabla Particiones (TP[])")
label2.grid(column=0,row=4)

#Tabla de particiones
tp = ttk.Treeview(root, height=5)
tp['columns'] = ('No', 'Localidad', 'Tamano', 'Estado', 'Proceso')
tp.column("#0", width=0, stretch=False)
tp.column("No", anchor=CENTER, width=80, stretch=False)
tp.column("Localidad", anchor=CENTER, width=80, stretch=False)
tp.column("Tamano", anchor=CENTER, width=80, stretch=False)
tp.column("Estado", anchor=CENTER, width=80, stretch=False)
tp.column("Proceso", anchor=CENTER, width=80, stretch=False)

tp.heading('#0', text='', anchor=CENTER)
tp.heading('No', text='No', anchor=CENTER)
tp.heading('Localidad', text='Localidad', anchor=CENTER)
tp.heading('Tamano', text='Tamaño', anchor=CENTER)
tp.heading('Estado', text='Estado', anchor=CENTER)
tp.heading('Proceso', text='Estado', anchor=CENTER)

tp.grid(column=0,row=5)

btn_text = StringVar()
btn = Button(root, textvariable=btn_text, command=siguientePaso)
btn_text.set("Paso "+str(paso))
btn.grid(column=1,row=6)

disponible = gm.siguiente_paso(paso)

label3 = Label(text="OS",bg="blue",width=30)
label3.grid(column=2,row=2)

label4 = Label(text="",bg="gray",width=30)
label4.grid(column=2,row=3,rowspan=3,sticky="ns")

root.mainloop()