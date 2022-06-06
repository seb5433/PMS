# GUI del administrador de proyectos

import json
from platform import release
from tkinter import *
import tkinter
from tkinter.ttk import Style, Treeview
from turtle import bgcolor, width
from backend.backend import Project
from customtkinter.widgets.ctk_canvas import CTkCanvas
from customtkinter.windows.ctk_tk import CTk
from tkcalendar import *
import tksheet as sheet
import customtkinter as ctk
import os
import sys
import datetime

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

        self.button_3 = ctk.CTkButton(master=self.frame_left, text="Reporte", command=self.button_event)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.button_4 = ctk.CTkButton(master=self.frame_left, text="Ir a inicio", command=self.ir_a_inicio)
        self.button_4.grid(row=5, column=0, pady=10, padx=20)

        self.logo_img = PhotoImage (file= os.path.join (self.PATH_IMAGE, "logo.png"))

        self.logo = Label(master=self.frame_left, image= self.logo_img, bg = self.COLOR_PRIMARIO)

        self.logo.grid(row=9, column=0, pady=10, padx=10)

        self.frame_right_calendar.rowconfigure((0), weight=1)

        today = datetime.date.today()
        mindate = datetime.date(year=2018, month=1, day=21)
        maxdate = today + datetime.timedelta(days=960)
        print(mindate, maxdate)

        cal = Calendar(self.frame_right_calendar, font="Cascade 13", selectmode='day', locale='es_ES', mindate=mindate, maxdate=maxdate, disabledforeground='red', cursor="hand2", year=2022, month=5, day=20)
        cal.pack(fill="both", expand=True)
        self.activity()

        self.MASTER.mainloop()


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

        
        self.activity_tree.tag_configure("odd", background = self.COLOR_FONDO, foreground= "#E7F3F3")
        self.activity_tree.tag_configure("even", background = self.COLOR_PRIMARIO, foreground= "#E7F3F3")

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
        for element in self.project.activitidades:
            parent = ''
            for relacion in self.project.relations:
                if element.id == relacion.next:
                    parent = relacion.preceding
                    space += 1

            tupla = (element.name, element.duration)
            
            if (x % 2 == 0):
                self.activity_tree.insert(parent, END, iid= f"{x}", values = tupla, tags= "odd")
            else:
                self.activity_tree.insert(parent, END, iid= f"{x}", values = tupla, tags= "even")
            x += 1

        self.activity_tree.column ("#0", minwidth=10, width = 20*space, stretch = True)

    def click_izq (self, event):
        font = ('Segoe UI', 13,)
        menu = Menu (self.frame_right_activity, tearoff= 0, title= "Manejo de actividades", relief= "flat")
        menu.add_command (label= "Nueva actividad", font = font, command = self.open_crear_actividad)
        menu.add_command (label= "Eliminar actividad", font = font, )
        menu.post(event.x_root, event.y_root)

    def deselect_all (self, event):
        if len(self.activity_tree.selection()) > 0:
            self.activity_tree.selection_remove(self.activity_tree.selection()[0])

    def open_crear_actividad (self):
        self.frame_crear_actividad = ctk.CTkToplevel (bg = "#292E36")
        self.frame_crear_actividad.focus_force()
        self.frame_crear_actividad.wm_overrideredirect(True)
        self.frame_crear_actividad.resizable(0, 0)
        ancho = 400
        alto = 120
        width = 250
        self.frame_crear_actividad.geometry (f"{ancho}x{alto}")
        ctk.CTkLabel (self.frame_crear_actividad, text= "Crear actividad", text_font= ("Segoe UI", 15)).pack (side = TOP)
        frame_entries = ctk.CTkFrame (self.frame_crear_actividad, bg_color = "#292E36", fg_color= "#292E36")
        frame_entries.pack (side = TOP)
        self.nombre = ctk.CTkEntry (frame_entries, placeholder_text = "Nombre", width= width)
        self.nombre.bind ("<Return>", self.key_enter_activity)
        self.nombre.focus_set()
        self.nombre.pack (side = LEFT, pady = 10, padx = 10)
        self.duracion = ctk.CTkEntry (frame_entries, placeholder_text = "Duración", width= 120)
        self.duracion.bind ("<Return>", self.key_enter_activity)
        self.duracion.pack (side = LEFT, pady = 10, padx = 10)
        ctk.CTkButton (self.frame_crear_actividad, text = "Listo", fg_color = "#238636", cursor = "hand2", command = self.crear_actividad).pack (side = TOP, fill = "x", padx = 10)
        self.center(self.frame_crear_actividad)

    def key_enter_activity(self, event):
        self.crear_actividad()
    
    def crear_actividad (self):
        children = self.activity_tree.selection()
        
        id = self.project.new_activity (self.nombre.get(), self.duracion.get(), "2022-12-12")
        self.activity_tree.insert ("",END, values= (self.nombre.get(), self.duracion.get()), tags= "even")
        self.frame_crear_actividad.destroy()
        self.project.update()
        if len(children) > 0:
            self.project.new_relation (int(children[0]), id)
        self.cargar_actividades()
        pass


    def change_mode(self):
        if self.switch_2.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

class WindowProject(Parametros):
    """
    ## Clase que genera la pestaña para cargar nuevo proyecto
    ### Editor: Sebastian Vera
    """
    width = 600
    height = 600

    def __init__(self):
        super().__init__()

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

        button_FP = DateEntry(self.frame_FP, width=12, background="gray18",foreground="gray18", borderwidth=2, year=2022)
        button_FP.pack(padx=10, pady=10)

        self.button_cargar = ctk.CTkButton(master =self.frame, text= "GUARDAR DATOS", width=280, height=40, fg_color= "#3d5a80", command=self.button_event)
        self.button_cargar.place(relx=0.5, rely=0.9, anchor=CENTER)


    def button_event(self):
        """# Obtencion de datos para cargar"""
        print("Nombre:", self.nombre_proyecto.get(), "Descripcion:", self.descripcion_proyecto.get())
    
    


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
                self.data.append ([proyecto.name, proyecto.description, proyecto.startdate, "0%"])
                self.IDES.append (x)
                x+=1
        
        

    def desplegar_tabla (self):
        
        self.tabla_proyectos = sheet.Sheet(self.frame_down,headers = ['Proyecto', 'Descripción', 'Inicio', 'Avance'],data= self.data,
        show_table = True,
        show_top_left = False,
        show_row_index = False,
        show_header = True,
        show_x_scrollbar = True,
        show_y_scrollbar = False,
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

        self.btn_eliminar = ctk.CTkButton(master=self.frame_botones,text="Eliminar",text_font=("Cascade", 14),width=120,height=40,
                                                border_width=1,corner_radius=5,cursor="hand2")
        self.btn_eliminar.grid(row=0, column=2,padx=13)

    def abrir (self):
        project = self.LISTA_PROYECTOS[self.row]
        self.frame_calendario.tkraise()
        App (self.frame_calendario, self, project)

    def nuevo_proyecto (self):
        WindowProject()

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
        self.RAIZ.config (menu = self.menu)
        fileMenu = Menu(self.menu)
        self.menu.add_cascade(label="Configuracion", menu=fileMenu, hidemargin= True)
        fileMenu.add_command(label="Feriados")
        fileMenu.add_command(label="Dias laborales")

        Portada(self.RAIZ, lista_proyectos)



        self.RAIZ.mainloop()
        
    
if __name__ == "__main__":
    Main()

    