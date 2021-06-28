import tkinter
from tkinter import *
from tkinter import ttk
from grafico import GraficoMemoria
from ttkbootstrap import *
from tkinter import messagebox


# Diccionario de la tabla de procesos
data = {'A':[8,1,7,0],
        'B':[14,2,7,0],
        'C':[18,3,4,0],
        'D':[6,4,6,0],
        'E':[14,5,5,0]
        }

# Gráfico de memoria
# Inicializar con datos, tamaño del OS y tamaño de memoria restante
gm = GraficoMemoria(data, 10, 54)

# Paso del proceso
paso = 0

# Bandera para terminar la ejecucion
terminar = False

#Callback del boton para cada paso
def siguientePaso():
    global terminar
    if terminar:
        messagebox.showinfo(message="Han finalizado todos los procesos.", title="Simulación Finalizada")
        root.destroy()        
        return

    global paso
    paso += 1
    btn_text.set("Paso: "+str(paso))

    #Borrar las tablas
    tp.delete(*tp.get_children())
    count_tp = 1

    tal.delete(*tal.get_children())
    count_tal = 1
    
    #Obtener listas de los espacios de memoria
    memoria, listo = gm.siguiente_paso(paso)

    #Doble bandera para que se muestre bien el paso final
    if listo:
        terminar = True

    for espacio in memoria:
        #Si hay un proceso
        if espacio[0]:
            tp.insert(parent='', index=count_tp, iid=count_tp, text='', values=(count_tp,espacio[1], espacio[3],'Ocupado',espacio[4]))
            count_tp +=1
        #Si es area libre
        else:
            tal.insert(parent='', index=count_tal, iid=count_tal, text='', values=(count_tal,espacio[1],espacio[3],'Libre'))
            count_tal +=1

    # Redibujar gráfico de memoria
    dibujar_memoria(rep_grafica, 64, 10, tp, tal)


def dibujar_memoria(canvas, memoria_total, tamaño_OS, tabla_procesos_activos, tabla_areas_libres):
    # Limpiar canvas
    canvas.delete("all")

    # Obtener dimensiones del canvas
    c_height = int(canvas["height"])
    c_width = int(canvas["width"])

    # Memoria SO
    x0 = (c_width * 0.35) / 2
    y0 = 0
    x1 = ((c_width * 0.35) / 2) + (c_width * 0.65)
    y1 = (tamaño_OS / memoria_total) * c_height
    memoria_SO_rectangle = canvas.create_rectangle(x0, y0, x1, y1, fill="#006AC5")
    memoria_SO_label = canvas.create_text((x0+x1)/2, (y0+y1)/2, text="SO", fill="white", font=("Helvetica", 10, "bold"), anchor=CENTER)
    memoria_SO_base_label = canvas.create_text(x0-5, y0, text="0K", fill="black", font=("Cambria", 9), anchor=NE)
    memoria_SO_limite_label = canvas.create_text(x0-5, y1, text=str(tamaño_OS)+"K", fill="black", font=("Cambria", 9), anchor=E)
    memoria_SO_tamaño_line = canvas.create_line(x1 - 4, y0 + 3, x1 - 4, y1 - 3, width=2)
    memoria_SO_tamaño_label = canvas.create_text(x1 - 8, (y0 + y1) / 2, text=str(tamaño_OS)+"K", fill="black",font=("Cambria", 9), anchor=E)

    # Memoria procesos activos
    for iid in tabla_procesos_activos.get_children():
        datos_proceso = tabla_procesos_activos.item(iid)["values"]
        y0 = (datos_proceso[1] / memoria_total) * c_height
        y1 = ((datos_proceso[1] + datos_proceso[2]) / memoria_total) * c_height
        proceso_rectangle = canvas.create_rectangle(x0, y0, x1, y1, fill="#CDE9F1")
        proceso_label = canvas.create_text((x0+x1)/2, (y0+y1)/2, text=datos_proceso[4], fill="black", font=("Helvetica", 10, "bold"), anchor=CENTER)
        proceso_limite_label = canvas.create_text(x0-5, y1, text=str(datos_proceso[1]+datos_proceso[2])+"K", fill="black", font=("Cambria", 9), anchor=E)
        proceso_tamaño_line = canvas.create_line(x1-4, y0+3, x1-4, y1-3, width=2)
        proceso_tamaño_label = canvas.create_text(x1-8, (y0+y1)/2, text=str(datos_proceso[2])+"K", fill="black", font=("Cambria", 9), anchor=E)

    # Memoria áreas libres
    if(len(tabla_areas_libres.get_children()) == 1):
        # Si solo hay una área libre
        iid = tabla_areas_libres.get_children()[0]
        datos_area_libre = tabla_areas_libres.item(iid)["values"]
        y0 = (datos_area_libre[1] / memoria_total) * c_height
        y1 = ((datos_area_libre[1] + datos_area_libre[2]) / memoria_total) * c_height
        area_libre_rectangle = canvas.create_rectangle(x0, y0, x1, y1, fill="#CECDF1")
        area_libre_label = canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text="Área libre " + str(datos_area_libre[0]), fill="black", font=("Helvetica", 10, "bold"), anchor=CENTER)
        area_libre_limite_label = canvas.create_text(x0 - 5, y1, text=str(datos_area_libre[1] + datos_area_libre[2]) + "K", fill="black", font=("Cambria", 9), anchor=SE)
        area_libre_tamaño_line = canvas.create_line(x1 - 4, y0 + 3, x1 - 4, y1 - 3, width=2)
        area_libre_tamaño_label = canvas.create_text(x1 - 8, (y0 + y1) / 2, text=str(datos_area_libre[2])+"K", fill="black", font=("Cambria", 9), anchor=E)
    else:
        # Si hay más de una área libre (fragmentación)
        for iid in tabla_areas_libres.get_children():
            datos_area_libre = tabla_areas_libres.item(iid)["values"]
            y0 = (datos_area_libre[1] / memoria_total) * c_height
            y1 = ((datos_area_libre[1] + datos_area_libre[2]) / memoria_total) * c_height
            area_libre_rectangle = canvas.create_rectangle(x0, y0, x1, y1, fill="#F1CDD1")
            area_libre_label = canvas.create_text((x0+x1)/2, (y0+y1)/2, text="Área libre "+str(datos_area_libre[0]), fill="black", font=("Helvetica", 10, "bold"), anchor=CENTER)
            area_libre_limite_label = canvas.create_text(x0-5, y1, text=str(datos_area_libre[1]+datos_area_libre[2])+"K", fill="black", font=("Cambria", 9), anchor=SE)
            area_libre_tamaño_line = canvas.create_line(x1 - 4, y0 + 3, x1 - 4, y1 - 3, width=2)
            area_libre_tamaño_label = canvas.create_text(x1 - 8, (y0 + y1) / 2, text=str(datos_area_libre[2])+"K", fill="black", font=("Cambria", 9), anchor=E)
        # Etiqueta de fragmentación
        frag_label = canvas.create_text(c_width, c_height/2, text="Fragmentación", fill="#670902", font=("Helvetica", 10, "bold"), anchor=S, angle=90)

    # [FIX] Dibujar línea inferior del último rectángulo
    last_rectangle_bottom_line = canvas.create_line(x0, c_height-1, x1, c_height-1)



###########################################################

# Instanciar y configurar ventana (root)
root = Tk()
root_style = Style(theme="litera")
root.title("MVT")
root.geometry("722x612")
root.resizable(False, False)

# Título
label0 = Label(text="SIMULACIÓN DE ASIGNACIÓN DE MEMORIA CON MVT", font=("Helvetica", "17"))
label0.grid(row=0, column=0, columnspan=2, padx=60, pady=(10, 5))

# Tabla de procesos
frame_tabla_procesos = LabelFrame(text="Tabla de procesos", labelanchor="nw")
frame_tabla_procesos.grid(row=1, column=0, columnspan=2, sticky="NS", padx=15, pady=(0, 10))
tabla_procesos = ttk.Treeview(frame_tabla_procesos, height=5, columns=("Proceso", "Tamano", "Tiempo", "Duracion"))
tabla_procesos.column("#0", width=0, stretch=False)
tabla_procesos.column("Proceso", anchor=CENTER, width=110, stretch=False)
tabla_procesos.column("Tamano", anchor=CENTER, width=110, stretch=False)
tabla_procesos.column("Tiempo", anchor=CENTER, width=120, stretch=False)
tabla_procesos.column("Duracion", anchor=CENTER, width=110, stretch=False)
tabla_procesos.heading("#0", text="", anchor=CENTER)
tabla_procesos.heading("Proceso", text="Proceso", anchor=CENTER)
tabla_procesos.heading("Tamano", text="Tamaño", anchor=CENTER)
tabla_procesos.heading("Tiempo", text="Tiempo de llegada", anchor=CENTER)
tabla_procesos.heading("Duracion", text="Duración", anchor=CENTER)
for i, key in enumerate(data):
    tabla_procesos.insert(parent="", index=i, iid=i, text="",
                          values=(key, str(data[key][0]) + "K", data[key][1], data[key][2]))
tabla_procesos.grid(row=0, column=0, padx=5, pady=(3, 7))

# Tabla de areas libres
frame_tal = LabelFrame(text="Tabla de áreas libres", labelanchor="nw")
frame_tal.grid(row=2, column=0, sticky="NSEW", padx=(15, 0), pady=(0, 10))
tal = ttk.Treeview(frame_tal, height=5, columns=("No", "Localidad", "Tamano", "Estado"))
tal.column("#0", width=0, stretch=False)
tal.column("No", anchor=CENTER, width=95, stretch=False)
tal.column("Localidad", anchor=CENTER, width=95, stretch=False)
tal.column("Tamano", anchor=CENTER, width=95, stretch=False)
tal.column("Estado", anchor=CENTER, width=95, stretch=False)
tal.heading("#0", text="", anchor=CENTER)
tal.heading("No", text="No", anchor=CENTER)
tal.heading("Localidad", text="Localidad", anchor=CENTER)
tal.heading("Tamano", text="Tamaño", anchor=CENTER)
tal.heading("Estado", text="Estado", anchor=CENTER)
espacios = gm.espacios[0]
tal.insert(parent="", index=1, iid=1, text="", values=(1, espacios[1], espacios[3], "Libre"))
tal.grid(row=0, column=0, padx=5, pady=(3, 7))

# Tabla de particiones
frame_tp = LabelFrame(text="Tabla de particiones", labelanchor="nw")
frame_tp.grid(row=3, column=0, sticky="NSEW", padx=(15, 0))
tp = ttk.Treeview(frame_tp, height=5, columns=("No", "Localidad", "Tamano", "Estado", "Proceso"))
tp.column("#0", width=0, stretch=False)
tp.column("No", anchor=CENTER, width=80, stretch=False)
tp.column("Localidad", anchor=CENTER, width=75, stretch=False)
tp.column("Tamano", anchor=CENTER, width=75, stretch=False)
tp.column("Estado", anchor=CENTER, width=75, stretch=False)
tp.column("Proceso", anchor=CENTER, width=75, stretch=False)
tp.heading("#0", text="", anchor=CENTER)
tp.heading("No", text="No", anchor=CENTER)
tp.heading("Localidad", text="Localidad", anchor=CENTER)
tp.heading("Tamano", text="Tamaño", anchor=CENTER)
tp.heading("Estado", text="Estado", anchor=CENTER)
tp.heading("Proceso", text="Proceso", anchor=CENTER)
tp.grid(row=0, column=0, padx=5, pady=(3, 7))

# Botón de pasos
btn_text = StringVar()
btn_text.set("Paso: " + str(paso))
btn = Button(textvariable=btn_text, command=siguientePaso, padx=7)
btn.grid(row=4, column=0, columnspan=2, pady=15)

# Representación gráfica
frame_rep_grafica = LabelFrame(text="Representación gráfica", labelanchor="nw")
frame_rep_grafica.grid(row=2, column=1, rowspan=2, sticky="NSEW", padx=(15, 15))
rep_grafica = Canvas(frame_rep_grafica, height=300, width=273, borderwidth=0, highlightthickness=0)
rep_grafica.grid(row=0, column=0, padx=(3, 0), pady=(6, 3))
dibujar_memoria(rep_grafica, 64, 10, tp, tal)

disponible = gm.siguiente_paso(paso)

root.mainloop()

#pyinstaller --onefile main.py --collect-all ttkbootstrap