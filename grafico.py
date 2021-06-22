from tkinter import *
from tkinter import ttk

class GraficoMemoria:

    def __init__(self, data, inicio, maxmem):
        
        #Datos
        self.data = data
        
        #Cantidad de memoria restante (aun no checa fragmentacion)
        self.memoria = maxmem
        
        #Espacios de memoria
        #0 = libre 1 = ocupado, localidad inicio, localidad fin, tamano, letra/nombre del proceso 
        self.espacios = [[0, inicio, inicio + maxmem, maxmem,'']]
        
        #Cola de acciones a realizar (cargar o descargar un proceso)
        self.cola = []


    def siguiente_paso(self,paso):

        #Primero checar las acciones pendientes
        self.atender_cola()

        if not self.data:
            #Terminar el programa
            print("FIN")
            self.reordenar_memoria()
            return self.espacios

        #Checar los procesos en el diccionario de datos
        for key, proceso in self.data.items():

            #Es un paso anterior y no ha sido añadido el proceso
            if paso == proceso[1] - 1 and not proceso[3]:
                #Preparar para añadir
                self.anadir_cola(key,1)
                #Marcar como añadido
                proceso[3] = 1
                
                print("Paso "+str(paso)+": Añadiendo "+key)
                print()

            #Es un paso anterior a la eliminacion del proceso
            elif paso == proceso[1] + proceso[2] - 2:
                #Preparar para eliminar
                self.anadir_cola(key,0)
                print("Paso "+str(paso)+": Eliminando "+key)
                print()
            else:
                continue

        self.reordenar_memoria()

        return self.espacios

    def ocupar_memoria(self, nombre, proceso):

        for idx, espacio in enumerate(self.espacios):
            #Esta libre el espacio y tiene mayor tamaño que el proceso
            #Fragmentar una parte para que la ocupe el proceso
            if not espacio[0] and espacio[3] >= proceso[0]:
                old_espacio = espacio.copy()
                self.espacios[idx] = [1, old_espacio[1], old_espacio[1]+proceso[0],proceso[0],nombre]
                self.espacios.insert(idx+1,[0,old_espacio[1]+proceso[0],old_espacio[2],old_espacio[3]-proceso[0],''])
                print(self.espacios)
                break

    def desocupar_memoria(self,nombre):
        for idx, espacio in enumerate(self.espacios):
            #Encontrar el espacio en el que se encuentra el proceso
            if espacio[4] == nombre:
                self.espacios[idx][0] = 0
                print(self.espacios)

    def reordenar_memoria(self):
        copiaespacios = self.espacios.copy()
        cambio = False
        todel = 0
        for idx, espacio in enumerate(self.espacios):
            if idx == len(self.espacios)-1:
                break
            espacio_sig = self.espacios[idx+1]
            if espacio[0] == 0 and espacio_sig[0] == 0:
                copiaespacios[idx][0] = 0                           #No ocupado
                copiaespacios[idx][1] = espacio[1]                  #Inicio del primero
                copiaespacios[idx][2] = espacio_sig[2]              #Fin del segundo
                copiaespacios[idx][3] = espacio[3] + espacio_sig[3] #Tamaño combinado
                copiaespacios[idx][4] = ''                  #No asignado
                cambio = True
                todel = idx+1
                break
        if cambio:
            del copiaespacios[todel]
            self.espacios = copiaespacios.copy()
            self.reordenar_memoria()
    
    def anadir_cola(self,nombre,accion):
        self.cola.append([nombre,accion])

    def atender_cola(self):
        if not self.cola:
            return

        #Backup para quitar los procesos terminados del dic de datos
        newdata = self.data.copy()

        #A veces no se puede realizar la primera accion en la cola (como por falta de espacio)
        #Iterar hasta que una se pueda
        for idx, todo in enumerate(self.cola):
            nombre = todo[0]
            accion = todo[1]
            proceso = self.data[nombre]

            if accion:
                #Se carga el proceso a memoria
                
                #En el caso de que no alcance la memoria
                if self.memoria < proceso[0]:
                    #Incrementar el tiempo de llegada y hacer otra accion
                    proceso[1] += 1
                    continue
                
                self.memoria -= proceso[0]
                self.data[nombre][3] = 1
                self.ocupar_memoria(nombre, proceso)
            else:
                #Se desocupa el proceso
                self.memoria += proceso[0]
                self.desocupar_memoria(nombre)
                #Se elimina el proceso listo del dic de datos
                del newdata[nombre]

            self.data = newdata.copy()
            self.cola.pop(idx)

            break