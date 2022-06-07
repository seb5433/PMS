
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

