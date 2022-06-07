import json
import tkinter as tk
from tkinter import ttk


from .date_entry import *
import os
from datetime import timedelta

#Librerias para el camino criticoy diagrama de Gantt
import numpy as np
from .caminocritico import Node
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from .reporte import *
from PIL import Image



class Project():
    def __init__(self, nombre, numero, descripcion, fecha):
        self.nombre = nombre
        self.id = numero
        self.descripcion = descripcion
        self.fecha_inicio = fecha
        self.actividades = []
        self.relaciones = []

    """
    Metodos de manejo de proyectos
    """
    #Despliega la informacion del proyecto
    def __view_project(self):
        print('\n')
        self.project_resume()
        print(f'Descripcion: {self.descripcion}')
        print(f'Fecha de inicio: {self.fecha_inicio}')
    
    #Despliega el ID y nombre del proyecto
    def project_resume(self):
        print(f"ID: [{self.id}] Nombre: {self.nombre}")
    
    #Metodo de clase para agregar un proyecto nuevo
    @classmethod
    def add_project(cls, lista_proyectos, nombre, descripcion, fecha):
        with open("config/config.json", "r") as file:
            info = json.load(file)
            config = info["id"] + 1
        lista_proyectos.append(Project(nombre, config, descripcion, fecha))
        lista_proyectos[-1].update()
        with open("config/config.json", "w") as file:
            info["id"] = config
            json.dump(info, file, indent = 4)

        return lista_proyectos
    
    #Metodo para eliminar un proyecto completo
    @classmethod
    def del_project(cls, lista_proyectos, numero):
        ident = None
        for k in range(len(lista_proyectos)):
            if (lista_proyectos[k].id == numero):
                ident = k
        if ident != None:
            del lista_proyectos[ident]
            os.remove("./data/p_"+str(numero)+".json")
        return lista_proyectos

    #Metodo de clase para desplegar la descripcion de
    #los proyectos
    @classmethod
    def projects_view(cls, lista_poyectos):
        for project in lista_poyectos:
            project.__view_project()
    
    #Metodo de clase para desplegar la lista de proyectos
    #con su nombre y ID
    @classmethod
    def projects_list(cls, lista_proyectos):
        for project in lista_proyectos:
            print(f"[{project.id}] Nombre: {project.nombre}")

    """
    Metodos de manejo para las actividades
    """
    #Metodo para AGREGAR una nueva actividad al objeto 
    #tipo proyecto
    def new_activity(self, nombre, duracion, fecha):
        if len(self.actividades) == 0:
            numero = 0
        else:
            numero = self.actividades[-1].id + 1
        self.actividades.append(Activity(nombre, numero, 
                                            duracion, fecha))
        self.update()
        return numero

    #Metodo para cargar las actividades desde los JSON
    #desde la funcion dowload()
    def load_activity(self, nombre, numero, duracion, fecha):
        self.actividades.append(Activity(nombre, numero, 
                                            duracion, fecha))

    #Metodo para visualizar la descripcion de las actividades
    #de un proyecto
    def view_activities(self):
        for activity in self.actividades:
            activity.activity_description()
    
    #Metodo para visualizar la lista de activiades
    #de un proyecto
    def activities_list(self):
        for activity in self.actividades:
            activity.activity_resume()

    #Metodo para eliminar una actividad
    def del_activity(self, numero):
        ident = None
        for k in range (len(self.actividades)):
            if self.actividades[k].id == numero:
                ident = k
        if ident != None:
            del self.actividades[ident]
            self.update()
            self.del_relation2(numero)

    #Metodo para obtener la lista con los IDs de las actividades
    #que estan en el camino critico de un proyecto, osea tienen que
    #hacer self.actividades_criticas nomas y verificar 
    #si str(actividad.id) in self.actividades+_criticas() es False
    def actividades_criticas(self):
        p = Node("")
        for k in self.actividades:
            p.add(Node(str(k.id), duration = int(k.duracion)))
        for k in self.relaciones:
            p.link(str(k.preceding), str(k.next))
        p.update_all()
        camino = [str(n) for n in p.get_critical_path()]
        return camino

    #Metodo para desplegar el diagrama de Gantt
    def diagrama(self):
        camino = self.actividades_criticas()
        
        with open("config/diagrama.csv", "w", encoding = "utf-8") as FILE:
            FILE.write("name,start,end,critical")
            for actividad in self.actividades:
                FILE.write(f"\n{actividad.nombre},{actividad.fecha_inicio},{actividad.fecha_inicio + timedelta(days = int(actividad.duracion))},{is_critic(str(actividad.id), camino)}")

        csv = pd.read_csv("config/diagrama.csv")
        
        csv["start"] = pd.to_datetime(csv["start"], format = "%Y-%m-%d")
        csv["end"] = pd.to_datetime(csv["end"], format = "%Y-%m-%d")
        
        csv.sort_values("start", axis=0, ascending=True, inplace=True)
        csv.reset_index(drop=True, inplace= True)
        
        color_dict = {'y':'red', 'n':'blue'}
        
        csv["Duration"] = csv["end"] - csv["start"] + timedelta(days = 1)
        
        csv["PastTime"] = csv["start"] - csv["start"][0]
        
        nrow = len(csv)
        
        plt.figure(num = 1, figsize = (10, 6), dpi = 100)
        bar_width = 0.9
        
        for i in range (nrow):
            i_rev = nrow - 1 - i
            plt.broken_barh([(csv["start"][i_rev], csv["Duration"][i_rev])], (i - bar_width / 2, bar_width), color = color_dict[str(csv["critical"][i_rev])])
            plt.broken_barh([(csv["start"][0], csv["PastTime"][i_rev])], (i - bar_width / 2, bar_width), color = "white")
        
        y_pos = np.arange(nrow)
        
        plt.yticks(y_pos, labels= reversed(csv["name"]))
        
        #Poner en formato MES-dias
        """locale.setlocale(locale.LC_TIME, 'es_ES')
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(fmt= "%b-%y"))
        plt.gca().xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))"""
        
        
        plt.grid(axis="x", which="major", lw=1)
        plt.grid(axis="x", which="minor", ls="--", lw=1)
        
        plt.gcf().autofmt_xdate(rotation=30)
        plt.xlim(csv["start"][0],)
        plt.xlabel("Fecha", fontsize=12, weight="bold")
        plt.title(f"Diagrama de Gantt - Proyecto: {self.nombre}", fontsize = 12, weight = "bold")
        plt.tight_layout(pad=0.8)
        
        #Anexar leyendas
        leyend_dict = {"Camino critico" : "red", "Actividad no critica" : "blue"}
        leyenda = [Patch(facecolor=leyend_dict[i], label=i)  for i in leyend_dict]
        plt.legend(handles=leyenda)

        plt.savefig('images/gant.jpg')

    def generarReporte(self):
        self.diagrama()
        
        datos = []
        
        for activity in self.actividades:
            lista = {"NOMBRE" : activity.nombre, 
                        "DURACION" : str(activity.duracion), 
                        "FECHA DE INICIO" : str(activity.fecha_inicio),
                        "FECHA DE FINALIZACION": str(activity.fecha_inicio + timedelta(days= int(activity.duracion)))}
            datos.append(lista)
            

        titulo = f"Proyecto: {self.nombre}"
        
        cabecera = (("NOMBRE", "NOMBRE"),
            ("DURACION", "DURACION"),
            ("FECHA DE INICIO", "FECHA DE INICIO"),
            ("FECHA DE FINALIZACION", "FECHA DE FINALIZACION"))

        nombrePDF = "Reporte.pdf"

        reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
        #print(reporte)

    """
    Metodos de manejo de relaciones
    """
    #Metodo para crear una nueva relacion en un proyecto
    def new_relation(self, precedente, siguiente):
        if len(self.relaciones) == 0:
            numero = 0
        else:
            numero = self.relaciones[-1].id + 1
        for k in range(len(self.actividades)):
            if self.actividades[k].id == precedente:
                pre = k
            if self.actividades[k].id == siguiente:
                sig = k

        with open ("config/feriados.json", "r") as FILE:
            feriados = json.loads(FILE.read())

        day = self.actividades[pre].fecha_inicio + timedelta(days = int(self.actividades[pre].duracion))
        no_laborales = []
        for x in range (len(feriados["feriados"])):
            no_laborales.append (f"{int(feriados['feriados'][x].split('/')[0])}/{int(feriados['feriados'][x].split('/')[1])}")

        while (self.calular_dia(day.year, day.month, day.day) in feriados["dias_no_laborales"] or f"{day.day}/{day.month}" in no_laborales):
            day = day + timedelta(days = 1)
        self.actividades[sig].fecha_inicio = day
        self.relaciones.append(Relation(numero, precedente, siguiente))
        self.update()

    #Metodo para visualizar las relaciones
    def view_relations(self):
        for relation in self.relaciones:
            relation.relation_description()

    #Metodo para visualizar las relaciones    
    def relations_list(self):
        for relation in self.relaciones:
            print(f"ID: {relation.id} Precedente: {relation.precedent} Siguiente: {relation.next}")

    def del_relation2(self, numero):
        ident = []
        for k in range (len(self.relaciones)):
            if self.relaciones[k].preceding == numero or self.relaciones[k].next == numero:
                ident.append(k)
        for k in ident:
            del self.relaciones[k]
            self.update()
                
    
    #Metodo para cargar las relaciones en un proyecto
    #mediante la funcion download()
    def load_relation(self, numero, precedente, siguiente):
        self.relaciones.append(Relation(numero, precedente, siguiente))

    


    """

    Método update para actualizar el JSON del proyecto

    """
    #Este metodo actualiza el archivo JSON correspondiente al
    #proyecto seleccionado reescribiendo toda la informacion 
    def update(self):
        exportproject = {"nombre" : self.nombre, 
                    "id" : self.id, 
                    "descripcion" : self.descripcion,
                    "startdate" : self.fecha_inicio, 
                    "actividades" : [], 
                    "relaciones" : [] }

        for activity in self.actividades:
            activities = {"nombre" : activity.nombre, "id" : activity.id, 
                        "duracion" : activity.duracion, 
                        "fechaini" : activity.fecha_inicio}
            exportproject["actividades"].append(activities)
        
        for relation in self.relaciones:
            relations = {"id" : relation.id,
                        "pre" : relation.preceding, 
                        "sig" : relation.next}   
            exportproject["relaciones"].append(relations)
        
        with open("data/p_"+str(self.id)+".json", "w") as file:
            json.dump(exportproject, file, indent = 4, default=str)

    def calular_dia (self, year, month, date):
        month_kode = [1,4,4,0,2,5,0,3,6,1,4,6]
        year_kode = [0,6,4,2,0,6]
        day_kode = [0,1,2,3,4,5,6]
        a1 = 0
        a2 = 0
        a3 = 0
        a4 = 0
        a5 = 0

        year2 = year

        a1 = date
        month = month - 1
        month = month_kode[month]
        a2 = month


        if year>=1500 and year<=1599:
            year2 = year_kode[0]

        if year>=1600 and year<=1699:
            year2 = year_kode[1]

        if year>=1700 and year<=1799:
            year2 = year_kode[2]

        if year>=1800 and year<=1899:
            year2 = year_kode[3]

        if year>=1900 and year<=1999:
            year2 = year_kode[4]

        if year>=2000 and year<=2099:
            year2 = year_kode[5]

        a3 = year2
        a4 = year % 100
        a5 = a4 / 4
        a5 = int(a5)
        a6 = a1 + a2 + a3 + a4 + a5
        a7 = a6 % 7
        a8 = 0
        a8 = day_kode[a7]
        if a8 == 0:
            return "SABADO"
        if a8 == 1:
            return "DOMINGO"
        if a8 == 2:
            return "LUNES"
        if a8 == 3:
            return "MARTES"
        if a8 == 4:
            return "MIERCOLES"
        if a8 == 5:
            return "JUEVES"
        if a8 == 6:
            return "VIERNES"

"""
Clase de actividades
"""
class Activity():
    def __init__(self, nombre, numero, duracion, fecha):
        self.nombre = nombre
        self.id = numero
        self.duracion = duracion
        self.fecha_inicio = fecha
    """
    Metodos de las actividades
    """
    #Metodo para describir la actividad
    def activity_description(self):
        print("\n")
        self.activity_resume()
        print(f"Inicio: {self.fecha_inicio}")
        print(f"Duracion: {self.duracion}")

    #Metodo que resume el ID y el nombre de la actividad
    def activity_resume(self):
        print(f"ID: {self.id} Nombre: {self.nombre}")


"""
Clase de relaciones
"""
class Relation():
    def __init__(self, numero, precedente, siguiente):
        self.id = numero
        self.preceding = precedente
        self.next = siguiente

    #Metodo para describir una relacion
    def relation_description(self):
        print(f"ID: {self.id}")
        print(f"Precendente: {self.preceding} Siguiente: {self.next}")


"""
Clase feriado 
"""
class Feriado():
 
    def new_feriado(self,feriados,dias,nuevo_feriado):
        self.dias_no_laborales=[]
        self.nuevo_feriado=nuevo_feriado
        bandera=self.validar_feriado(nuevo_feriado)
        if bandera==1:
            if nuevo_feriado in feriados:
                print("El feriado ya se encuentra actualmente\n")
            else:    
                feriados.append(nuevo_feriado)
                with open("config/"+"feriados.json","w") as file:
                        dict={'feriados':feriados,'dias_no_laborales':dias}
                        file.write(json.dumps(dict))
                print("El feriado se agrego correctamente")        

    def borrar_feriados(self,feriados,dias,borrar_feriado):
        self.dias_no_laborales=[]
        self.borrar_feriado=borrar_feriado
        if borrar_feriado in feriados:
            feriados.remove(borrar_feriado)
            print("El feriado fue eliminado correctamente\n")
            with open("config/"+"feriados.json","w") as file:
                dict={'feriados':feriados,'dias_no_laborales':dias}
                file.write(json.dumps(dict))
        else:
            print("El feriado no existe\n")   

    def new_no_laboral(self,feriados,dias,nuevo_no_laboral):
        nuevo_no_laboral = nuevo_no_laboral.upper()
        self.nuevo_no_laboral=nuevo_no_laboral
        if nuevo_no_laboral in dias:
            print("El dia ya se encuentra agregado\n")
        else:    
            dias.append(nuevo_no_laboral)
            with open("config/"+"feriados.json","w") as file:
                    dict={'feriados':feriados,'dias_no_laborales':dias}
                    file.write(json.dumps(dict))
            print("El dia no laboral se agrego correctamente") 

    def borrar_dia_no_laboral(self,feriados,dias,borrar_dia):
        borrar_dia = borrar_dia.upper()
        self.borrar_dia=borrar_dia
        if borrar_dia in dias:
            dias.remove(borrar_dia)
            print("El dia no laboral fue eliminado correctamente\n")
            with open("config/"+"feriados.json","w") as file:
                dict={'feriados':feriados,'dias_no_laborales':dias}
                file.write(json.dumps(dict))
        else:
            print("El dia no laboral no existe\n")
    def validar_feriado(self,nuevo_feriado):
        self.meses= (0,31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        self.cant_meses=["01","02","03","04","05","06","07","08","09","10","11","12"]
        POS = nuevo_feriado.index("/")
        MES = nuevo_feriado[POS+1:]
        dia=nuevo_feriado[0:POS]
        if MES in self.cant_meses:
            if MES[0]=="0":
                MES=int(MES[0]+MES[1])
            else:
                MES=int(MES)
            if dia[0]=="0":
                dia=int(dia[0]+dia[1])
            else:
                dia=int(dia)
            if(MES >= 1 and MES <= 12):
                if(dia >= 1 and dia <= self.meses[MES]):
                    bandera=1 
                    return bandera
                else:
                    bandera=0
                    return bandera
            else:
                    bandera=0
                    return bandera


"""
Función que despliega el selector de fechas
"""
def seleccionar_fecha(func):
    def imprimir():
        func(cal.get_date())        
        top.destroy()
    top = tk.Tk()
    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2022)
    cal.pack(padx=10, pady=10)
    ttk.Button(top, text="Seleccionar", command = imprimir).pack()
    top.mainloop()

"""
Funcion para saber si una actividad se encuentra dentro del camino critico
"""
def is_critic(ident, camino):
    if ident in camino:
        return "y"
    else:
        return "n"




