
import json
import tkinter as tk
from tkinter import ttk
from .date_entry import *

class Project():
    def __init__(self, nombre, numero, descripcion, fecha):
        self.name = nombre
        self.id = numero
        self.description = descripcion
        self.startdate = fecha
        self.endingdate = None
        self.__activities = []
        self.__relations = []

    """
    Metodos de manejo de proyectos
    """
    #Despliega la informacion del proyecto
    def __view_project(self):
        print('\n')
        self.project_resume()
        print(f'Descripcion: {self.description}')
        print(f'Fecha de inicio: {self.startdate}')
        print(f"Fecha de finalizacion: {self.endingdate}")
    
    #Despliega el ID y nombre del proyecto
    def project_resume(self):
        print(f"ID: [{self.id}] Nombre: {self.name}")
    
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
        k = 0
        for project in lista_proyectos:
            print(f"[{k}] Nombre: {project.name}")
            k += 1

    """
    Metodos de manejo para las actividades
    """
    #Metodo para AGREGAR una nueva actividad al objeto 
    #tipo proyecto
    def new_activity(self, nombre, duracion, fecha):
        if len(self.__activities) == 0:
            numero = 0
        else:
            numero = self.__activities[-1].id + 1
        self.__activities.append(Activity(nombre, numero, 
                                            duracion, fecha))
        self.update()

    #Metodo para cargar las actividades desde los JSON
    #desde la funcion dowload()
    def load_activity(self, nombre, numero, duracion, fecha, fechaf):
        self.__activities.append(Activity(nombre, numero, 
                                            duracion, fecha))
        self.late_start = fechaf

    #Metodo para visualizar la descripcion de las actividades
    #de un proyecto
    def view_activities(self):
        for activity in self.__activities:
            activity.activity_description()
    
    #Metodo para visualizar la lista de activiades
    #de un proyecto
    def activities_list(self):
        for activity in self.__activities:
            activity.activity_resume()

    """
    Metodos de manejo de relaciones
    """
    #Metodo para crear una nueva relacion en un proyecto
    def new_relation(self, precedente, siguiente):
        if len(self.__relations) == 0:
            numero = 0
        else:
            numero = self.__relations[-1].id + 1
        self.__relations.append(Relation(numero, precedente, siguiente))
        self.update()

    #Metodo para visualizar las relaciones
    def view_relations(self):
        for relation in self.__relations:
            relation.relation_description()

    #Metodo para visualizar las relaciones    
    def relations_list(self):
        for relation in self.__relations:
            print(f"ID: {relation.id} Precedente: {relation.precedent} Siguiente: {relation.next}")

    #Metodo para cargar las relaciones en un proyecto
    #mediante la funcion download()
    def load_relation(self, numero, precedente, siguiente):
        self.__relations.append(Relation(numero, precedente, siguiente))

    


    """

    Método update para actualizar el JSON del proyecto

    """
    #Este metodo actualiza el archivo JSON correspondiente al
    #proyecto seleccionado reescribiendo toda la informacion 
    def update(self):
        exportproject = {"nombre" : self.name, 
                    "id" : self.id, 
                    "descripcion" : self.description,
                    "startdate" : self.startdate, 
                    "endingdate" : self.endingdate, 
                    "actividades" : [], 
                    "relaciones" : [] }

        for activity in self.__activities:
            activities = {"nombre" : activity.name, "id" : activity.id, 
                        "duracion" : activity.duration, 
                        "fechaini" : activity.early_start, 
                        "fechafi" : activity.late_start}
            exportproject["actividades"].append(activities)
        
        for relation in self.__relations:
            relations = {"id" : relation.id,
                        "pre" : relation.preceding, 
                        "sig" : relation.next}   
            exportproject["relaciones"].append(relations)
        
        with open("data/p_"+str(self.id)+".json", "w") as file:
            json.dump(exportproject, file, indent = 4)



"""
Clase de actividades
"""
class Activity():
    def __init__(self, nombre, numero, duracion, fecha):
        self.name = nombre
        self.id = numero
        self.duration = duracion
        self.early_start = fecha
        self.late_start = self.early_start
    """
    Metodos de las actividades
    """
    #Metodo para describir la actividad
    def activity_description(self):
        print("\n")
        self.activity_resume()
        print(f"Inicio: {self.late_start}")
        print(f"Duracion: {self.duration}")

    #Metodo que resume el ID y el nombre de la actividad
    def activity_resume(self):
        print(f"ID: {self.id} Nombre: {self.name}")


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
Clase feriado que no sirve para nada
"""
class Feriado():
    def __init__(self):
        self.fechas = ["0101", "0103", "0105", "1505", "1206", "1508", "2908", "0812", "2512"]



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





