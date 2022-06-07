# GUI del administrador de proyectos
import json
from tkinter import *
from tkinter.ttk import Style, Treeview
from backend.backend import Project
from tkcalendar import *
import tksheet as sheet
import customtkinter as ctk
import os
import sys
import datetime
from backend.backend import *

#AGREGADO POR SEBAS VERA
from PIL import Image, ImageTk


class Parametros ():
    def __init__(self) -> None: 
        self.ANCHO = '1120'
        self.ALTO  = '600'
        self.COLOR_FONDO = "#1C2128" 
        self.COLOR_PRIMARIO = "#22272E"
        self.COLOR_FG = "#768390"
        self.COLOR_LINEAS = "#316DCA"
        self.COLOR_SELECCION = "#264779"
        self.PATH = self.resource_path()
        self.PATH_IMAGE = os.path.join (self.PATH,'images')
        self.PATH_CONFIG = os.path.join (self.PATH,'config')
        self.PATH_DATA = os.path.join (self.PATH,'data')

    def resource_path(self):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path)

    def center(self, win):
        """
        ## Función que centra una ventana en la pantalla
        - param win: la ventana principal o frame a centrar
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()


class App(Parametros):

    def __init__(self, master, parent, project):
        super().__init__()
        self.project = project
        self.PARTENT = parent
        self.MASTER = master
        self.MASTER.grid_columnconfigure(1, weight=1)
        self.MASTER.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self.MASTER,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right_activity = ctk.CTkFrame(master=self.MASTER)
        self.frame_right_activity.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.frame_right_calendar = ctk.CTkFrame(master=self.MASTER)
        self.frame_right_calendar.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_right_activity.grid_rowconfigure(1, minsize=10)   # empty row with minsize as spacing

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(6, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = ctk.CTkLabel(master=self.frame_left, text="Navegación", text_font=("Roboto Medium", -20), text_color = "white",)  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = ctk.CTkButton(master=self.frame_left, text="Calendario", command=self.open_calendario)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = ctk.CTkButton(master=self.frame_left, text="Actividades", command=self.open_actividades)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = ctk.CTkButton(master=self.frame_left, text="Reporte", command=self.generar_reporte)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.button_4 = ctk.CTkButton(master=self.frame_left, text="Ir a inicio", command=self.ir_a_inicio)
        self.button_4.grid(row=5, column=0, pady=10, padx=20)

        self.logo_img = PhotoImage (file= os.path.join (self.PATH_IMAGE, "logo.png"))

        self.logo = Label(master=self.frame_left, image= self.logo_img, bg = self.COLOR_PRIMARIO)

        self.logo.grid(row=9, column=0, pady=10, padx=10)

        self.frame_right_calendar.rowconfigure(0, weight=1)
        self.frame_right_calendar.grid_columnconfigure(0, weight=1)

        today = datetime.date.today()
        self.mindate = datetime.date(year=2018, month=1, day=21)
        self.maxdate = today + datetime.timedelta(days=960)

        self.activity()
        with open(os.path.join(self.PATH_CONFIG, "feriados.json"), 'r') as json_file:
            self.feriados = json.loads(json_file.read())        
        
        self.project_calendar(self.feriados)
        self.MASTER.mainloop()

    
    #identifica si existe una actividad en esa fecha
    def cantidad_actividades(self, date):
        i = 0
        for p in self.project.actividades:  
            if str(p.fecha_inicio) == str(date):
                i += 1
        return i
                    
    #identifica los datos de las actividades
    def actividades(self,date, i):
        self.date = date
        i = i
        self.nombres = []
        self.duration = []
        self.fechas = []
        for p in self.project.actividades:
            if str(p.fecha_inicio) == str(date):
                self.nombres.append(p.nombre)
                self.duration.append(p.duracion)
                self.fechas.append(p.fecha_inicio)
        return self.nombres[i], self.duration[i], self.fechas[i]

    #display label con datos de la actividad en la fecha seleccionada
    def cal_event(self, event):
        self.frame_actividades = ctk.CTkFrame(master=self.frame_right_calendar, width=500, height=90, fg_color = self.COLOR_PRIMARIO)
        self.frame_actividades.grid(row=1, column=0, sticky="nswe")
        self.date_calendar = (event.widget.selection_get())
        n = self.cantidad_actividades(self.date_calendar)
        self.frame_actividades.grid_rowconfigure(n, weight=1)
        self.frame_actividades.grid_columnconfigure(0, weight=1)
        self.frame_actividades.grid_propagate(False)
        if n > 0:   
            for i in range(n):
                self.actividades(self.date_calendar, i)
                self.event_name = ctk.CTkLabel(master=self.frame_actividades, corner_radius=5, text= self.nombres[i], text_font=("Cascade", 12)) 
                self.event_name.grid(row=i, column=0, sticky="nswe", pady=2, padx=2)
                self.event_date = ctk.CTkLabel(master=self.frame_actividades, corner_radius=5, text= self.fechas[i], text_font=("Cascade", 12)) 
                self.event_date.grid(row=i, column=1, sticky="nswe", pady=2, padx=2)
                self.event_duration = ctk.CTkLabel(master=self.frame_actividades, corner_radius=5, fg_color=("white"), text="Duración: " + self.duration[i], text_font=("Cascade", 12), text_color="gray18")
                self.event_duration.grid(row=i, column=2, sticky="nswe", pady=2, padx=2)
        
        else:
            self.event_none=ctk.CTkLabel(master=self.frame_actividades, corner_radius=10, height=20, fg_color=("#1D1F28"), text="No hay actividades para esta fecha " , text_font=("Cascade", 20), text_color="#FFFFFF")
            self.event_none.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")
            
    def identificar_dia_de_la_semana(self, dia):
        self.dia = dia
        self.dia_semana = []
        for i in range(len(self.dia['dias_no_laborales'])):
            if ((self.dia['dias_no_laborales'][i]).lower()) == "domingo":
                self.dia_semana.append(7)
            elif ((self.dia['dias_no_laborales'][i]).lower()) == "lunes":
                self.dia_semana.append(1)
            elif ((self.dia['dias_no_laborales'][i]).lower()) == "martes":
                self.dia_semana.append(2)
            elif ((self.dia['dias_no_laborales'][i]).lower()) == "miercoles":
                self.dia_semana.append(3)
            elif ((self.dia['dias_no_laborales'][i]).lower()) == "jueves":
                self.dia_semana.append(4)
            elif ((self.dia['dias_no_laborales'][i]).lower()) == "viernes":
                self.dia_semana.append(5)
            elif ((self.dia['dias_no_laborales'][i]).lower()) == "sabado":
                self.dia_semana.append(6)
        return self.dia_semana.sort()


    def project_calendar(self, feriados): 
        """### Identificar los dias no laborales"""

        #abre feriados.json
        self.feriados = feriados
        #display calendar
        self.cal = Calendar(self.frame_right_calendar, font="Cascade 13", selectmode='day', locale='es_ES',
                mindate= self.mindate, maxdate= self.maxdate, 
                weekenddays = self.identificar_dia_de_la_semana(self.feriados),
                othermonthbackground = "#5D6466",
                othermonthforeground = "#FFFFFF",
                cursor="hand2",
                year=2022,
                month=5,
                day=20,
                date_pattern='y-mm-dd',
                fg_color=self.COLOR_LINEAS,
                background = self.COLOR_PRIMARIO,
                disabledbackground="red",
                bordercolor="#B5BAB8", 
                headersbackground="#1D1F28",
                normalbackground="#22272E",
                foreground='#FFFFFF',
                normalforeground='#FFFFFF',
                headersforeground='white',
                weekendbackground="#3F464A",
                weekendforeground='white',
                disabledforeground='#FFFFFF'
                )
        self.cal.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        self.cal.rowconfigure(0, weight=1)
        self.cal.columnconfigure(0, weight=1)
        #click izquierdo para mostrar actividades
        self.cal.bind("<<CalendarSelected>>", self.cal_event)

        self.fechas= []
        for i in self.project.actividades:
            self.fechas.append(str(i.fecha_inicio))
        
        for i in range (len(self.fechas)):
            self.date = datetime.datetime.strptime(self.fechas[i], '%Y-%m-%d').date()
            self.cal.calevent_create(self.date, text=self.fechas[i], tags = "activity")
            self.cal.tag_config("activity", background='#2ea043', foreground='#FFFFFF')
        
        self.mindate_int = self.mindate.strftime('%Y')
        self.maxdate_int = self.maxdate.strftime('%Y')
        self.years = int(self.maxdate_int) - int(self.mindate_int) 
        
        for i in self.feriados['feriados']:
            for j in range (self.years):
                self.year = int(self.mindate_int) + j
                self.date = datetime.datetime.strptime(i, '%d/%m').date()
                self.date = self.date.replace(year=self.year)
                self.cal.calevent_create(self.date, tags=i, text=i)
                self.cal.tag_config(i, background='#da5b0b', foreground='#FFFFFF')


    def generar_reporte (self):
        self.project.generarReporte()

    def button_event(self):
        pass
    
    def open_actividades (self):
        self.frame_right_activity.tkraise()

    def open_calendario (self):
        self.frame_right_calendar.tkraise()
    
    def ir_a_inicio (self):
        self.PARTENT.frame_portada.tkraise()

    def fixed_map(self, option):
        return [elm for elm in self.style.map('Treeview', query_opt=option) if 
        elm[:2] != ('!disabled', '!selected')]

 
    def activity (self):
        """## Funcion que crea la pestaña de actividades"""
        
        # Creacion del estilo para la treeview
        self.style = Style ()
        self.style.theme_use ("vista")
        self.style.map('Treeview', foreground= self.fixed_map('foreground'), background= [('selected', self.COLOR_SELECCION)], filedbackground = self.fixed_map('filedbackground'))
        self.style.configure("Treeview", background = self.COLOR_PRIMARIO, filedbackground = "black", highlightthickness=0, bd=0, font=('Segoe UI', 11)) # Modify the font of the body
        self.style.configure("Treeview.Heading", font=('Segoe UI', 13,'bold'), background = "#1C2128",  bd=0) # Modify the font of the headings
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        

        columns = ("Actividad", "Duracion")
        self.activity_tree =  Treeview(self.frame_right_activity,columns = columns, style="Treeview",height=20)
        self.activity_tree.pack (side = TOP, pady = 5, fill = "x")


        gama = 30
        for x in range(1,21):
            factor = x*20
            self.activity_tree.tag_configure(f"{x}", background = self.to_hex((gama+factor, gama+factor, gama+factor)), foreground= "#E7F3F3")


        self.activity_tree.heading ("#0", )
        self.activity_tree.heading ("Actividad", text= "Actividad")
        self.activity_tree.heading ("Duracion", text= "Duración")

        self.activity_tree.column ("Actividad", minwidth=500, width = 500)
        self.activity_tree.column ("Duracion", minwidth=250, width = 350)

        self.activity_tree.bind ("<Button-3>",self.click_izq)
        self.activity_tree.bind ("<Escape>",self.deselect_all)
        self.cargar_actividades()



    def cargar_actividades (self):
        # add data to the treeview
        for x in self.activity_tree.get_children():
            self.activity_tree.delete(x)

        x = 0
        space = 0
        for element in self.project.actividades:
            parent = ''
            for relacion in self.project.relaciones:
                if element.id == relacion.next:
                    parent = relacion.preceding
                    space += 1

            tupla = (element.nombre, element.duracion)
            parent_ = parent
            z = 1
            while (self.activity_tree.parent (parent_) != ""):
                z+=1
                parent_ = self.activity_tree.parent (parent_)

            self.activity_tree.insert(parent, END, iid= f"{element.id}", values = tupla, tags = f"{z}")

        self.activity_tree.column ("#0", minwidth=10, width = 20*space, stretch = True)

    def click_izq (self, event):
        font = ('Segoe UI', 13,)
        menu = Menu (self.frame_right_activity, tearoff= 0, title= "Manejo de actividades", relief= "flat")
        menu.add_command (label= "Nueva actividad", font = font, command = lambda: self.open_crear_actividad("Crear actividad", self.crear_actividad))
        menu.add_command (label= "Editar actividad", font = font, command = lambda: self.open_crear_actividad("Editar actividad", self.editar_actividad))
        menu.add_command (label= "Eliminar actividad", font = font, )
        menu.post(event.x_root, event.y_root)

    def deselect_all (self, event):
        if len(self.activity_tree.selection()) > 0:
            self.activity_tree.selection_remove(self.activity_tree.selection()[0])

    def open_crear_actividad (self, titulo, callback):
        self.frame_crear_actividad = ctk.CTkToplevel (bg = "#292E36")
        self.frame_crear_actividad.focus_force()
        self.frame_crear_actividad.wm_overrideredirect(True)
        self.frame_crear_actividad.resizable(0, 0)
        ancho = 400
        alto = 120
        width = 250
        self.frame_crear_actividad.geometry (f"{ancho}x{alto}")
        ctk.CTkLabel (self.frame_crear_actividad, text= titulo, text_font= ("Segoe UI", 15)).pack (side = TOP)
        frame_entries = ctk.CTkFrame (self.frame_crear_actividad, bg_color = "#292E36", fg_color= "#292E36")
        frame_entries.pack (side = TOP)
        self.var_nombre = StringVar()
        self.nombre = ctk.CTkEntry (frame_entries,textvariable = self.var_nombre, placeholder_text = "Nombre", width= width)
        self.nombre.bind ("<Return>", callback)
        self.nombre.focus_set()
        self.nombre.pack (side = LEFT, pady = 10, padx = 10)
        self.var_duracion = StringVar()
        self.duracion = ctk.CTkEntry (frame_entries, textvariable = self.var_duracion, placeholder_text = "Duración", width= 120)
        self.duracion.bind ("<Return>", callback)
        self.duracion.pack (side = LEFT, pady = 10, padx = 10)
        ctk.CTkButton (self.frame_crear_actividad, text = "Listo", fg_color = "#238636", cursor = "hand2", command = callback).pack (side = TOP, fill = "x", padx = 10)
        self.center(self.frame_crear_actividad)

        if ("Editar" in titulo):
            id = self.activity_tree.selection()[0]
            element = self.activity_tree.item(id)
            print ("Edicion")
            #self.nombre.config (text = element["values"][0])
            self.var_nombre.set (element["values"][0])
            #self.duracion.config (text = element["values"][1])
            self.var_duracion.set (element["values"][1])
    
    def crear_actividad (self, event = None):
        children = self.activity_tree.selection()
        
        id = self.project.new_activity (self.nombre.get(), self.duracion.get(), self.project.fecha_inicio)
        self.activity_tree.insert ("",END, values= (self.nombre.get(), int(self.duracion.get())), tags= "even")
        self.frame_crear_actividad.destroy()
        self.project.update()
        if len(children) > 0:
            self.project.new_relation (int(children[0]), id)
        self.cargar_actividades()
        pass

    def editar_actividad (self, event):
        children = self.activity_tree.selection()
        print ("Cargando actividades")
        children = int(children[0])
        object = 0
        for x in self.project.actividades:
            if children == x.id:
                object = x
        object.nombre = self.nombre.get()
        object.duracion = self.duracion.get()
        self.frame_crear_actividad.destroy()
        self.project.update()
        self.cargar_actividades()

    def change_mode(self):
        if self.switch_2.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    def to_hex (self, rgb):
	    return '#' + ''.join('%02x'%i for i in rgb).upper()

class WindowProject(Parametros):
    """
    ## Clase que genera la pestaña para cargar nuevo proyecto
    ### Editor: Sebastian Vera
    """
    width = 600
    height = 600

    def __init__(self, parent_properties = None,lista_proyectos = None):
        super().__init__()
        self.parent_properties = parent_properties

        self.MASTER = ctk.CTkToplevel()
        self.MASTER.geometry(f"{WindowProject.width}x{WindowProject.height}")
        self.MASTER.minsize(WindowProject.width, WindowProject.height)
        self.MASTER.maxsize(WindowProject.width, WindowProject.height)
        self.center (self.MASTER)


        # cargar imagen de fondo
        image = Image.open(os.path.join(self.PATH_IMAGE, "fondo.jpg")).resize((self.width, self.height))
        self.bg_image = ImageTk.PhotoImage(image)
        self.image_label = Label(self.MASTER, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)


        # main frame
        self.frame = ctk.CTkFrame(self.MASTER, width=300, height=WindowProject.height, corner_radius=10)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)


        # projechub logo
        logo = Image.open(os.path.join(self.PATH_IMAGE,"logo.png")).resize((136,32))
        self.projechub = ImageTk.PhotoImage(logo)
        self.projechub_label = Label(self.frame, image=self.projechub)
        self.projechub_label.config(bg="gray18")
        self.projechub_label.place(relx=0.3, rely=0.1)


        # Nombre del Proyecto
        self.frame_NP = ctk.CTkFrame(master=self.frame, width=220, height=70, corner_radius=20)
        self.frame_NP.place(relx=0.5, rely=0.2, anchor=N)

        self.label_NP = ctk.CTkLabel(self.frame_NP, corner_radius=10, width=200, height=30, fg_color=("#3d5a80"), text="Nombre del Proyecto")
        self.label_NP.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.nombre_proyecto = ctk.CTkEntry(master=self.frame_NP, width=200, placeholder_text="nuevo_proyecto")
        self.nombre_proyecto.place(relx=0.5, rely=0.75, anchor=CENTER)


        # Descripcion del Proyecto
        self.frame_DP = ctk.CTkFrame(master=self.frame, corner_radius=20, width=220, height=200)
        self.frame_DP.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.label_DP = ctk.CTkLabel(master=self.frame_DP, corner_radius=20, width=200, height=20, fg_color=("#3d5a80"), text="Descripcion del Proyecto")
        self.label_DP.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.descripcion_proyecto = ctk.CTkEntry(master=self.frame_DP, width=200, height=150, placeholder_text="descripcion_proyecto", bg="gray18")
        self.descripcion_proyecto.place(relx=0.5, rely=0.55, anchor=CENTER)


        # Fecha de Inicio
        self.frame_FP = ctk.CTkFrame(self.frame, width=220, height=50, corner_radius=20)
        self.frame_FP.place(relx=0.5, rely=0.76, anchor=CENTER)

        self.label_FP = ctk.CTkLabel(self.frame_FP, width=200, height=20, text="Fecha de Inicio", fg_color="#3d5a80")
        self.label_FP.place(relx=0.5, rely=0.25, anchor=CENTER)

        self.button_FP = DateEntry(self.frame_FP, width=12, background="gray18",foreground="gray18", borderwidth=2, year=2022)
        self.button_FP.pack(padx=10, pady=10)

        self.button_cargar = ctk.CTkButton(master =self.frame, text= "GUARDAR DATOS", width=280, height=40, fg_color= "#3d5a80", command=lambda:self.button_event(lista_proyectos))
        self.button_cargar.place(relx=0.5, rely=0.9, anchor=CENTER)


    def button_event(self,lista_proyectos):
        """# Obtencion de datos para cargar"""
        nombre = self.nombre_proyecto.get()
        descripcion = self.descripcion_proyecto.get()
        fecha = self.button_FP.get_date()
        lista = Project.add_project(lista_proyectos, nombre, descripcion, fecha)
        self.parent_properties.LISTA_PROYECTOS = lista
        self.parent_properties.data_manage()
        self.parent_properties.draw_data()
        self.MASTER.destroy()
    
    


class Portada (Parametros):
    """## Clase que genera una portada"""

    def __init__(self, master, lista_proyectos = None) -> None:
        super().__init__()
        self.MASTER = master
        self.LISTA_PROYECTOS = lista_proyectos
        
        self.data_manage ()

        self.MASTER.rowconfigure(0, weight=1)
        self.MASTER.columnconfigure(0, weight=1)

        self.frame_calendario = Frame (self.MASTER, bg = self.COLOR_FONDO)
        self.frame_calendario.grid(row = 0, column = 0, sticky= "nsew")
        
        self.frame_portada = Frame (self.MASTER, bg = self.COLOR_FONDO)
        self.frame_portada.grid( row = 0, column = 0, sticky= "nsew",)
        

        self.frame_up = Frame (self.frame_portada, bg = self.COLOR_PRIMARIO)
        self.frame_down = Frame (self.frame_portada, bg = self.COLOR_PRIMARIO, cursor = "hand2")
        self.frame_up.pack (side = TOP, padx = 10, pady = 10, fill = "both")
        self.frame_down.pack (side = TOP, padx = 10, fill = "both",expand=True)
        self.desplegar_tabla()
        self.buscador()
        #self.abrir()

        self.MASTER.mainloop()

    def data_manage (self):
        self.data = []
        self.IDES = []
        x = 0
        if self.LISTA_PROYECTOS:
            for proyecto in self.LISTA_PROYECTOS:
                #print (proyecto.nombre)
                self.data.append ([proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, "0%"])
                self.IDES.append (x)
                x+=1
        
    def draw_data (self):
        #TODO: Arreglar esta cagada
        self.tabla_proyectos.destroy()
        self.desplegar_tabla()

    def desplegar_tabla (self):
        
        self.tabla_proyectos = sheet.Sheet(self.frame_down,headers = ['Proyecto', 'Descripción', 'Inicio', 'Avance'], data = self.data,
        show_table = True,
        show_top_left = False,
        show_row_index = False,
        show_header = True,
        show_x_scrollbar = False,
        show_y_scrollbar = True,
        width = None,
        height = None,
        default_header = "letters", #letters, numbers or both
        default_row_index = "numbers", #letters, numbers or both
        ##show_default_header_for_empty = True,
        page_up_down_select_row = True,
        expand_sheet_if_paste_too_big = True,
        paste_insert_column_limit = None,
        paste_insert_row_limit = None,
        ##ctrl_keys_over_dropdowns_enabled = False,
        arrow_key_down_right_scroll_page = False,
        enable_edit_cell_auto_resize = True,
        data_reference = None,
        startup_select = None,
        startup_focus = True,
        total_columns = None,
        total_rows = None,
        column_width = 10,
        header_height = "1",
        max_colwidth = "inf",
        max_rh = "inf",
        max_header_height = "inf",
        max_row_width = "inf",
        row_index = None,
        after_redraw_time_ms = 100,
        row_index_width = 100,
        auto_resize_default_row_index = True,
        set_all_heights_and_widths = False,
        row_height = "2",
        align = "w",
        header_align = "center",
        row_index_align = "center",
        displayed_columns = [],
        all_columns_displayed = True,
        max_undos = 20,
        outline_thickness = 0,
        column_drag_and_drop_perform = True,
        row_drag_and_drop_perform = True,
        empty_horizontal = 0,
        empty_vertical = 0,
        show_vertical_grid = True,
        show_horizontal_grid = True,
        display_selected_fg_over_highlights = False,
        show_selected_cells_border = False, 
        theme = "dark",
        popup_menu_fg                      = "gray2",
        popup_menu_bg                      = "#f2f2f2",
        popup_menu_highlight_bg            = "#91c9f7",
        popup_menu_highlight_fg            = "black",
        frame_bg                           = self.COLOR_FONDO, # COLOR_FONDO DEL FONDO DE LA TABLA
        table_grid_fg                      = self.COLOR_PRIMARIO, # COLOR_FONDO DE LAS LINEAS DE SEPARACION
        table_bg                           = "#292E36", # COLOR_FONDO FONDO DE TABLA PARTE DATOS
        table_fg                           = self.COLOR_FG, 
        table_selected_cells_border_fg     = self.COLOR_FONDO,
        table_selected_cells_bg            = self.COLOR_FONDO,
        table_selected_cells_fg            = self.COLOR_FG,
        
        table_selected_rows_border_fg      = self.COLOR_FG,
        table_selected_rows_bg             = self.COLOR_FG,
        table_selected_rows_fg             = self.COLOR_FG,
        table_selected_columns_border_fg   = self.COLOR_LINEAS,
        table_selected_columns_bg          = self.COLOR_FONDO,
        table_selected_columns_fg          = self.COLOR_FG,
        
        resizing_line_fg                   = self.COLOR_FONDO,
        #drag_and_drop_bg                   = theme_light_blue['drag_and_drop_bg'],
        index_bg                           = self.COLOR_FONDO,
        index_border_fg                    = self.COLOR_FG,
        index_grid_fg                      = self.COLOR_FONDO,
        index_fg                           = self.COLOR_FG,
        index_selected_cells_bg            = self.COLOR_FONDO,
        index_selected_cells_fg            = self.COLOR_FG,
        index_selected_rows_bg             = self.COLOR_FONDO,
        index_selected_rows_fg             = self.COLOR_FG,
        index_hidden_rows_expander_bg      = self.COLOR_FONDO,

        header_bg                          = self.COLOR_FONDO,
        header_border_fg                   = self.COLOR_FONDO,
        header_grid_fg                     = self.COLOR_FONDO,
        header_fg                          = self.COLOR_FG,
        header_selected_cells_bg           = self.COLOR_FONDO,
        header_selected_cells_fg           = self.COLOR_FG,
        header_selected_columns_bg         = self.COLOR_FONDO,
        header_selected_columns_fg         = self.COLOR_FG,
        header_hidden_columns_expander_bg  = self.COLOR_FONDO,
        top_left_bg                        = self.COLOR_FONDO,
        top_left_fg                        = self.COLOR_FONDO,
        top_left_fg_highlight              = self.COLOR_FONDO,
        )

        self.tabla_proyectos.header_font(newfont = ("Cascade", 10, "normal"))
        self.tabla_proyectos.enable_bindings()
        self.tabla_proyectos.header_align(align = "center", redraw = True)
        self.tabla_proyectos.align_columns(columns = [2,3], align = "center", align_header = True, redraw = True)
        self.tabla_proyectos.column_width(column = 0, width = 150, only_set_if_too_small = False, redraw = True)
        self.tabla_proyectos.column_width(column = 1, width = 630, only_set_if_too_small = False, redraw = True)
        self.tabla_proyectos.column_width(column = 2, width = 130, only_set_if_too_small = False, redraw = True)
        self.tabla_proyectos.column_width(column = 3, width = 120, only_set_if_too_small = False, redraw = True)
        #self.draw_data()
        
        self.tabla_proyectos.disable_bindings("all")
        self.tabla_proyectos.bind ("<ButtonPress-1>", self.selected)

        self.tabla_proyectos.row_index(newindex = self.IDES, index = None) # Colocacion de las IDES
        self.tabla_proyectos.pack ( fill = "both", padx = 20,pady = 5, expand = True)


    def selected (self, binded):
        self.row = self.tabla_proyectos.identify_row(binded)
        self.tabla_proyectos.dehighlight_all()
        self.tabla_proyectos.highlight_rows(rows = [self.row], bg = self.COLOR_SELECCION, fg = "Black", highlight_index = True, redraw = True)


    def buscador(self):
        
        #Funcion que despliega el buscador y los botones 
        
        # CREACION DE LA IMAGEN BUSCAR
        self.frame_buscador_child = ctk.CTkFrame(master=self.frame_up,fg_color=self.COLOR_PRIMARIO,width=10,height=50)
        self.frame_buscador_child.grid(row=0, column=0)

        self.frame_espacio_vacio = ctk.CTkFrame(master=self.frame_up,width=80,height=40,fg_color=self.COLOR_PRIMARIO)
        self.frame_espacio_vacio.grid(row=0,column=1)

        self.frame_botones = ctk.CTkFrame(master=self.frame_up,width=500,height=40,fg_color=self.COLOR_PRIMARIO)
        self.frame_botones.grid(row=0,column=2,columnspan=3)


        # CREACION DEL ENTRY

        self.entry_buscador = ctk.CTkEntry(master=self.frame_buscador_child,text_font=("Cascade", 12),placeholder_text="Buscar proyecto...",width=500,height=40, text_color= "#768390")
        self.entry_buscador.pack(padx=20)


        # CREACION DE LOS BOTONES
        self.btn_nuevo = ctk.CTkButton(master=self.frame_botones,text="Nuevo",text_font=("Cascade", 14),width=120,height=40,
                                                border_width=1,corner_radius=5,cursor="hand2", command= self.nuevo_proyecto)
        self.btn_nuevo.grid(row=0,column=0,pady=15,padx=20)

        self.btn_abrir = ctk.CTkButton(master=self.frame_botones,text="Abrir",text_font=("Cascade", 14),width=120,height=40,
                                                border_width=1,corner_radius=5,cursor="hand2", command = self.abrir, fg_color= "#238636")
        self.btn_abrir.grid(row=0, column=1,padx=15)

        self.btn_eliminar = ctk.CTkButton(master=self.frame_botones,text="Eliminar",text_font=("Cascade", 14),width=120,height=40, fg_color= "#DA3633",
                                                border_width=1,corner_radius=5,cursor="hand2", command=lambda:self.eliminar(self.LISTA_PROYECTOS))
        self.btn_eliminar.grid(row=0, column=2,padx=13)

    def abrir (self):
        project = self.LISTA_PROYECTOS[self.row]
        self.frame_calendario.tkraise()
        App (self.frame_calendario, self, project)

    def nuevo_proyecto (self):
        WindowProject(self, self.LISTA_PROYECTOS)

    def eliminar (self,lista_proyecto):
        project = self.LISTA_PROYECTOS[self.row]
        id = int (project.id)
        
        self.LISTA_PROYECTOS = Project.del_project(lista_proyecto,id)
        self.data_manage()
        self.draw_data()

class WindowFeriados(Parametros):
    """
    ## Clase que genera la pestaña para feriado
    """

    width = 600
    height = 600

    def __init__(self):
        super().__init__()


        # self.COLOR_FONDO = "#1C2128" 
        # self.COLOR_PRIMARIO = "#22272E"
        # self.COLOR_FG = "#768390"
        # self.COLOR_LINEAS = "#316DCA"

        
        self.feriado = Feriado()
        
        # Carga de feriados para el tksheet
        datos = []
        with open("config/"+"feriados.json","r") as file:
            JSON=json.loads(file.read())
            self.feriados=JSON['feriados'] 
            self.dias_no_laborales2=JSON['dias_no_laborales']
        for i in range (len(self.feriados)):
            datos.append([self.feriados[i]])



        self.MASTER = ctk.CTkToplevel()
        self.MASTER.geometry(f"{WindowFeriados.width}x{WindowFeriados.height}")
        self.MASTER.minsize(WindowFeriados.width, WindowFeriados.height)
        self.MASTER.maxsize(WindowFeriados.width, WindowFeriados.height)
        self.center (self.MASTER)


        # cargar imagen de fondo
        image = Image.open(os.path.join(self.PATH_IMAGE, "fondo.jpg")).resize((self.width, self.height))
        self.bg_image = ImageTk.PhotoImage(image)
        self.image_label = Label(self.MASTER, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)


        # main frame
        self.frame = ctk.CTkFrame(self.MASTER, width=300, height=WindowFeriados.height, corner_radius=10)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)


        # projechub logo
        logo = Image.open(os.path.join(self.PATH_IMAGE,"logo.png")).resize((136,32))
        self.projechub = ImageTk.PhotoImage(logo)
        self.projechub_label = Label(self.frame, image=self.projechub)
        self.projechub_label.config(bg="gray18")
        self.projechub_label.place(relx=0.3, rely=0.1)


        # Nuevo feriado
        self.frame_add = ctk.CTkFrame(master=self.frame, width=220, height=70, corner_radius=20)
        self.frame_add.place(relx=0.5, rely=0.2, anchor=N)

        self.label_add = ctk.CTkLabel(self.frame_add, corner_radius=10, width=200, height=30, fg_color=("#3d5a80"), text="Agregar nuevo feriado")
        self.label_add.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.feriado_add = ctk.CTkEntry(master=self.frame_add, width=200, placeholder_text="(dd/mm)")
        self.feriado_add.place(relx=0.5, rely=0.75, anchor=CENTER)

        # Eliminar feriado
        self.frame_del = ctk.CTkFrame(master=self.frame, corner_radius=20, width=220, height=70)
        self.frame_del.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.label_del = ctk.CTkLabel(master=self.frame_del, corner_radius=20, width=200, height=30, fg_color=("#3d5a80"), text="Eliminar feriado")
        self.label_del.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.feriado_del = ctk.CTkEntry(master=self.frame_del, width=200, height=30, placeholder_text="(dd/mm)", bg="gray18")
        self.feriado_del.place(relx=0.5, rely=0.75, anchor=CENTER)


        # Frame tksheet
        self.frame_tksheet = ctk.CTkFrame(master=self.frame,width=220,height=240,corner_radius=15)
        self.frame_tksheet.place(relx=0.5, rely=0.68, anchor=CENTER)

        self.tabla_feriados = sheet.Sheet(self.frame_tksheet,headers= ['Listado de los feriados'],data=datos,
        show_table = True,
        show_top_left = False,
        show_row_index = False,
        show_header = True,
        show_x_scrollbar = True,
        show_y_scrollbar = True,
        width = 220,
        height = 220,
        default_header = "letters", #letters, numbers or both
        default_row_index = "numbers", #letters, numbers or both
        ##show_default_header_for_empty = True,
        page_up_down_select_row = True,
        expand_sheet_if_paste_too_big = True,
        paste_insert_column_limit = None,
        paste_insert_row_limit = None,
        ##ctrl_keys_over_dropdowns_enabled = False,
        arrow_key_down_right_scroll_page = False,
        enable_edit_cell_auto_resize = True,
        data_reference = None,
        startup_select = None,
        startup_focus = True,
        total_columns = None,
        total_rows = None,
        column_width = 1,
        header_height = "1",
        max_colwidth = "inf",
        max_rh = "inf",
        max_header_height = "inf",
        max_row_width = "inf",
        row_index = None,
        after_redraw_time_ms = 100,
        row_index_width = 100,
        auto_resize_default_row_index = True,
        set_all_heights_and_widths = False,
        row_height = "1",
        #font = get_font(),
        #header_font = get_heading_font(),
        #popup_menu_font = get_font(),
        align = "center",
        header_align = "center",
        row_index_align = "center",
        displayed_columns = [],
        all_columns_displayed = True,
        max_undos = 20,
        outline_thickness = 0,
        #outline_color = theme_light_blue['outline_color'],
        column_drag_and_drop_perform = True,
        row_drag_and_drop_perform = True,
        empty_horizontal = 0,
        empty_vertical = 0,
        ##selected_rows_to_end_of_window = False,
        ##horizontal_grid_to_end_of_window = False,
        ##vertical_grid_to_end_of_window = False,
        show_vertical_grid = True,
        show_horizontal_grid = True,
        display_selected_fg_over_highlights = False,
        show_selected_cells_border = False,
        theme = "dark",
        popup_menu_fg                      = "gray2",
        popup_menu_bg                      = "#f2f2f2",
        popup_menu_highlight_bg            = "#91c9f7",
        popup_menu_highlight_fg            = "black",
        frame_bg                           = self.COLOR_FONDO, # COLOR_FONDO DEL FONDO DE LA TABLA
        table_grid_fg                      = self.COLOR_PRIMARIO, # COLOR_FONDO DE LAS LINEAS DE SEPARACION
        table_bg                           = "#292E36", # COLOR_FONDO FONDO DE TABLA PARTE DATOS
        table_fg                           = self.COLOR_FG, 
        table_selected_cells_border_fg     = self.COLOR_FONDO,
        table_selected_cells_bg            = self.COLOR_FONDO,
        table_selected_cells_fg            = self.COLOR_FG,
        
        table_selected_rows_border_fg      = self.COLOR_FG,
        table_selected_rows_bg             = self.COLOR_FG,
        table_selected_rows_fg             = self.COLOR_FG,
        table_selected_columns_border_fg   = self.COLOR_LINEAS,
        table_selected_columns_bg          = self.COLOR_FONDO,
        table_selected_columns_fg          = self.COLOR_FG,
        
        resizing_line_fg                   = self.COLOR_FONDO,
        #drag_and_drop_bg                   = theme_light_blue['drag_and_drop_bg'],
        index_bg                           = self.COLOR_FONDO,
        index_border_fg                    = self.COLOR_FG,
        index_grid_fg                      = self.COLOR_FONDO,
        index_fg                           = self.COLOR_FG,
        index_selected_cells_bg            = self.COLOR_FONDO,
        index_selected_cells_fg            = self.COLOR_FG,
        index_selected_rows_bg             = self.COLOR_FONDO,
        index_selected_rows_fg             = self.COLOR_FG,
        index_hidden_rows_expander_bg      = self.COLOR_FONDO,

        header_bg                          = self.COLOR_FONDO,
        header_border_fg                   = self.COLOR_FONDO,
        header_grid_fg                     = self.COLOR_FONDO,
        header_fg                          = self.COLOR_FG,
        header_selected_cells_bg           = self.COLOR_FONDO,
        header_selected_cells_fg           = self.COLOR_FG,
        header_selected_columns_bg         = self.COLOR_FONDO,
        header_selected_columns_fg         = self.COLOR_FG,
        header_hidden_columns_expander_bg  = self.COLOR_FONDO,
        top_left_bg                        = self.COLOR_FONDO,
        top_left_fg                        = self.COLOR_FONDO,
        top_left_fg_highlight              = self.COLOR_FONDO,
        )

        self.tabla_feriados.disable_bindings("all")
        self.tabla_feriados.header_font(newfont = ("Cascade", 10, "normal"))
        # self.tabla_feriados.enable_bindings()
        self.tabla_feriados.header_align(align = "center", redraw = True)
        # self.tabla_proyectos.align_columns(columns = [2,3], align = "center", align_header = True, redraw = True)
        self.tabla_feriados.column_width(column = 0,only_set_if_too_small = False, redraw = True,width=200)
        #self.tabla_proyectos.set_all_cell_sizes_to_text(redraw = True)
        self.tabla_feriados.pack (padx=7,pady=7)
       

        # Boton de GUARDAR
        self.button_cargar = ctk.CTkButton(master =self.frame, text= "GUARDAR", width=280, height=40, fg_color= "#3d5a80", command=self.button_event)
        self.button_cargar.place(relx=0.5, rely=0.95, anchor=CENTER)


    def button_event(self):
        """# Obtencion de datos para cargar"""
        #print("\nNuevo:", self.feriado_add.get(), "\nEliminar:", self.feriado_del.get())

        if self.feriado_add.get() != "":
            self.feriado.new_feriado(self.feriados,self.dias_no_laborales2,self.feriado_add.get())

        if self.feriado_del.get() != "":
            self.feriado.borrar_feriados(self.feriados,self.dias_no_laborales2,self.feriado_del.get())
            
        self.MASTER.destroy()

class WindowNoLaborales(Parametros):
    """
    ## Clase que genera la pestaña de los dias no laborales
    """    
    width = 600
    height = 600

    def __init__(self):
        super().__init__()


        # self.COLOR_FONDO = "#1C2128" 
        # self.COLOR_PRIMARIO = "#22272E"
        # self.COLOR_FG = "#768390"
        # self.COLOR_LINEAS = "#316DCA"

        
        self.feriado = Feriado()
        
        # Carga de feriados para el tksheet
        datos = []
        with open("config/"+"feriados.json","r") as file:
            JSON=json.loads(file.read())
            self.feriados=JSON['feriados'] 
            self.dias_no_laborales2=JSON['dias_no_laborales']
        for i in range (len(self.dias_no_laborales2)):
            datos.append([self.dias_no_laborales2[i]])

        self.MASTER = ctk.CTkToplevel()
        self.MASTER.geometry(f"{WindowNoLaborales.width}x{WindowNoLaborales.height}")
        self.MASTER.minsize(WindowNoLaborales.width, WindowNoLaborales.height)
        self.MASTER.maxsize(WindowNoLaborales.width, WindowNoLaborales.height)
        self.center (self.MASTER)


        # cargar imagen de fondo
        image = Image.open(os.path.join(self.PATH_IMAGE, "fondo.jpg")).resize((self.width, self.height))
        self.bg_image = ImageTk.PhotoImage(image)
        self.image_label = Label(self.MASTER, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)


        # main frame
        self.frame = ctk.CTkFrame(self.MASTER, width=300, height=WindowNoLaborales.height, corner_radius=10)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)


        # projechub logo
        logo = Image.open(os.path.join(self.PATH_IMAGE,"logo.png")).resize((136,32))
        self.projechub = ImageTk.PhotoImage(logo)
        self.projechub_label = Label(self.frame, image=self.projechub)
        self.projechub_label.config(bg="gray18")
        self.projechub_label.place(relx=0.3, rely=0.1)


        # Nuevo feriado
        self.frame_add = ctk.CTkFrame(master=self.frame, width=220, height=70, corner_radius=20)
        self.frame_add.place(relx=0.5, rely=0.2, anchor=N)

        self.label_add = ctk.CTkLabel(self.frame_add, corner_radius=10, width=200, height=30, fg_color=("#3d5a80"), text="Agregar dia no laboral")
        self.label_add.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.feriado_add = ctk.CTkEntry(master=self.frame_add, width=200, placeholder_text="Ej: Sabado...")
        self.feriado_add.place(relx=0.5, rely=0.75, anchor=CENTER)

        # Eliminar feriado
        self.frame_del = ctk.CTkFrame(master=self.frame, corner_radius=20, width=220, height=70)
        self.frame_del.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.label_del = ctk.CTkLabel(master=self.frame_del, corner_radius=20, width=200, height=30, fg_color=("#3d5a80"), text="Eliminar dia no laboral")
        self.label_del.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.feriado_del = ctk.CTkEntry(master=self.frame_del, width=200, height=30, placeholder_text="Ej: Sabado...", bg="gray18")
        self.feriado_del.place(relx=0.5, rely=0.75, anchor=CENTER)


        # Frame tksheet
        self.frame_tksheet = ctk.CTkFrame(master=self.frame,width=220,height=240,corner_radius=15)
        self.frame_tksheet.place(relx=0.5, rely=0.68, anchor=CENTER)

        self.tabla_dias = sheet.Sheet(self.frame_tksheet,headers= ['Listado de los dias no laborales'],data=datos,
        show_table = True,
        show_top_left = False,
        show_row_index = False,
        show_header = True,
        show_x_scrollbar = True,
        show_y_scrollbar = True,
        width = 220,
        height = 220,
        default_header = "letters", #letters, numbers or both
        default_row_index = "numbers", #letters, numbers or both
        ##show_default_header_for_empty = True,
        page_up_down_select_row = True,
        expand_sheet_if_paste_too_big = True,
        paste_insert_column_limit = None,
        paste_insert_row_limit = None,
        ##ctrl_keys_over_dropdowns_enabled = False,
        arrow_key_down_right_scroll_page = False,
        enable_edit_cell_auto_resize = True,
        data_reference = None,
        startup_select = None,
        startup_focus = True,
        total_columns = None,
        total_rows = None,
        column_width = 1,
        header_height = "1",
        max_colwidth = "inf",
        max_rh = "inf",
        max_header_height = "inf",
        max_row_width = "inf",
        row_index = None,
        after_redraw_time_ms = 100,
        row_index_width = 100,
        auto_resize_default_row_index = True,
        set_all_heights_and_widths = False,
        row_height = "1",
        #font = get_font(),
        #header_font = get_heading_font(),
        #popup_menu_font = get_font(),
        align = "center",
        header_align = "center",
        row_index_align = "center",
        displayed_columns = [],
        all_columns_displayed = True,
        max_undos = 20,
        outline_thickness = 0,
        #outline_color = theme_light_blue['outline_color'],
        column_drag_and_drop_perform = True,
        row_drag_and_drop_perform = True,
        empty_horizontal = 0,
        empty_vertical = 0,
        ##selected_rows_to_end_of_window = False,
        ##horizontal_grid_to_end_of_window = False,
        ##vertical_grid_to_end_of_window = False,
        show_vertical_grid = True,
        show_horizontal_grid = True,
        display_selected_fg_over_highlights = False,
        show_selected_cells_border = False,
        theme = "dark",
        popup_menu_fg                      = "gray2",
        popup_menu_bg                      = "#f2f2f2",
        popup_menu_highlight_bg            = "#91c9f7",
        popup_menu_highlight_fg            = "black",
        frame_bg                           = self.COLOR_FONDO, # COLOR_FONDO DEL FONDO DE LA TABLA
        table_grid_fg                      = self.COLOR_PRIMARIO, # COLOR_FONDO DE LAS LINEAS DE SEPARACION
        table_bg                           = "#292E36", # COLOR_FONDO FONDO DE TABLA PARTE DATOS
        table_fg                           = self.COLOR_FG, 
        table_selected_cells_border_fg     = self.COLOR_FONDO,
        table_selected_cells_bg            = self.COLOR_FONDO,
        table_selected_cells_fg            = self.COLOR_FG,
        
        table_selected_rows_border_fg      = self.COLOR_FG,
        table_selected_rows_bg             = self.COLOR_FG,
        table_selected_rows_fg             = self.COLOR_FG,
        table_selected_columns_border_fg   = self.COLOR_LINEAS,
        table_selected_columns_bg          = self.COLOR_FONDO,
        table_selected_columns_fg          = self.COLOR_FG,
        
        resizing_line_fg                   = self.COLOR_FONDO,
        #drag_and_drop_bg                   = theme_light_blue['drag_and_drop_bg'],
        index_bg                           = self.COLOR_FONDO,
        index_border_fg                    = self.COLOR_FG,
        index_grid_fg                      = self.COLOR_FONDO,
        index_fg                           = self.COLOR_FG,
        index_selected_cells_bg            = self.COLOR_FONDO,
        index_selected_cells_fg            = self.COLOR_FG,
        index_selected_rows_bg             = self.COLOR_FONDO,
        index_selected_rows_fg             = self.COLOR_FG,
        index_hidden_rows_expander_bg      = self.COLOR_FONDO,

        header_bg                          = self.COLOR_FONDO,
        header_border_fg                   = self.COLOR_FONDO,
        header_grid_fg                     = self.COLOR_FONDO,
        header_fg                          = self.COLOR_FG,
        header_selected_cells_bg           = self.COLOR_FONDO,
        header_selected_cells_fg           = self.COLOR_FG,
        header_selected_columns_bg         = self.COLOR_FONDO,
        header_selected_columns_fg         = self.COLOR_FG,
        header_hidden_columns_expander_bg  = self.COLOR_FONDO,
        top_left_bg                        = self.COLOR_FONDO,
        top_left_fg                        = self.COLOR_FONDO,
        top_left_fg_highlight              = self.COLOR_FONDO,
        )
        # self.tabla_dias.enable_bindings()
        self.tabla_dias.header_font(newfont = ("Cascade", 10, "normal"))
        self.tabla_dias.disable_bindings("all")
        self.tabla_dias.header_align(align = "center", redraw = True)
        # self.tabla_proyectos.align_columns(columns = [2,3], align = "center", align_header = True, redraw = True)
        self.tabla_dias.column_width(column = 0,only_set_if_too_small = False, redraw = True,width=219)
        #self.tabla_proyectos.set_all_cell_sizes_to_text(redraw = True)
        self.tabla_dias.pack (padx=7,pady=7)
       

        # Boton de GUARDAR
        self.button_cargar = ctk.CTkButton(master =self.frame, text= "GUARDAR", width=280, height=40, fg_color= "#3d5a80", command=self.button_event)
        self.button_cargar.place(relx=0.5, rely=0.95, anchor=CENTER)


    def button_event(self):
        """# Obtencion de datos para cargar"""

        # print("\nNuevo:", self.feriado_add.get(), "\nEliminar:", self.feriado_del.get())

        if self.feriado_add.get() != "":
            self.feriado.new_no_laboral(self.feriados,self.dias_no_laborales2,self.feriado_add.get())

        if self.feriado_del.get() != "":
            self.feriado.borrar_dia_no_laboral(self.feriados,self.dias_no_laborales2,self.feriado_del.get())
            

        self.MASTER.destroy()



class Main (Parametros):
    """## Clase que genera el frame principal"""

    def __init__(self, lista_proyectos = None) -> None:
        super().__init__()
        """### Creación y configuracion de la pagina principal"""


        ctk.set_default_color_theme(os.path.join (self.PATH_CONFIG, "custom_theme.json"))
        #self.RAIZ = Tk("Adminstrador de proyectos", "Administrador de proyectos")
        self.RAIZ = ctk.CTk()
        self.RAIZ.geometry(f'{self.ANCHO}x{self.ALTO}')
        self.RAIZ.resizable(False, False)
        self.RAIZ.title("Project hub")
        self.RAIZ.config(bg=self.COLOR_FONDO)
        self.center (self.RAIZ)

        self.menu = Menu (self.RAIZ)
        self.RAIZ.config (menu = self.menu,)
        fileMenu = Menu(self.menu, tearoff= False, font= ("Cascade", 10))
        self.menu.add_cascade(label="Configuracion", menu=fileMenu)
        fileMenu.add_command(label="Feriados", command=WindowFeriados)
        fileMenu.add_command(label="Dias laborales", command=WindowNoLaborales)

        Portada(self.RAIZ, lista_proyectos)

        self.RAIZ.mainloop()
        
    
if __name__ == "__main__":
    Main()

    