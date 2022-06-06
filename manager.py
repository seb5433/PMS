
from backend.backend import *
import json
import os
from datetime import date
import gui

PATH = os.getcwd()
DATA_PATH = os.path.join (PATH, "data")

feriados = Feriado()
lista_proyectos = []

def obtenerfecha(fechaget):
    global fecha 
    fecha = str(fechaget)

def strdate(string):
    string = string.replace('\x00', '').strip()
    y = int(string[0:4])
    m = int(string[5:7])
    d = int(string[8:10])
    print(y, m, d)
    fecha = date(y, m, d)
    return fecha




def download(id_def):
    lista_proyectos = []
    for count in range(0, id_def+1):
        if os.path.exists("data/p_" + str(count) + ".json"):
            with open(os.path.join (DATA_PATH, f"p_{count}.json"), "r") as file:
                info = json.load(file)
                lista_proyectos.append(Project(info["nombre"], info["id"], info["descripcion"], date.fromisoformat(info["startdate"])))
                actividades = info["actividades"]
                relaciones = info["relaciones"]
                for k in actividades:
                    lista_proyectos[-1].load_activity(k["nombre"], k["id"], k["duracion"], date.fromisoformat(k["fechaini"]))                   
                for k in relaciones:
                    lista_proyectos[-1].load_relation(k["id"], k["pre"], k["sig"])
    return lista_proyectos


with open("config/config.json") as config:
    end = json.load(config)
    id_def = end["id"]
    username = end["user"]
lista_proyectos = download(id_def)


GUI = gui.Main(lista_proyectos)




"""print(f"\n\nBienvenido {username} !\nOpciones:\n")
print("1- Añadir nuevo proyecto")
print("2- Ver todos los proyectos")
print("3- Operar con proyecto") 
print("0- Salir")
opcion = -1
while opcion != 0:
    opcion = int(input('Ingrese la opcion: '))
    print('\n')
    if opcion == 1:
        nombre = input("Nombre del proyecto: ")
        descripcion = input("Descripcion: ")
        seleccionar_fecha(obtenerfecha)
        print(f"Fecha de inicio: {fecha}")
        Project.add_project(lista_proyectos, nombre, descripcion, fecha)
    
    elif opcion == 2:
        Project.projects_view(lista_proyectos)
    
    elif opcion == 3:
        Project.projects_list(lista_proyectos)
        ident = int(input("Ingrese el id del proyecto a manipular: "))
        opcion2 = -1
        while opcion2 != 0:
            print("\n")
            print("1- Agregar actividad")
            print("2- Ver actividades")
            print("3- Agregar relacion")
            print("4- Ver relaciones")
            print("0- Volver al menu principal")

            opcion2 = int(input("Ingrese la opcion a realizar: "))
            
            if opcion2 == 1:
                nombre = input("Ingrese el nombre de la actividad: ")
                duracion = input("Ingrese la duracion: ")
                seleccionar_fecha(obtenerfecha)
                print(f"Fecha de inicio: {fecha}")
                lista_proyectos[ident].new_activity(nombre, duracion, fecha)
            
            elif opcion2 == 2:
                lista_proyectos[ident].view_activities()
            
            elif opcion2 == 3:
                lista_proyectos[ident].activities_list()
                pre = int(input("Ingrese el ID de la actividad precedente: "))
                sig = int(input("Ingrese el ID de la activadad siguiente: "))
                lista_proyectos[ident].new_relation(pre, sig)

            elif opcion2 == 4:
                lista_proyectos[ident].view_relations()

            elif opcion2 == 0:
                break
    elif opcion==0:
        exit("Adiosito")
"""




