# GUI del administrador de proyectos

from tkinter import *
from tkcalendar import *
import tksheet as sheet
import customtkinter as ctk
import os
import sys
import datetime

class Parametros ():
    def __init__(self) -> None: 
        self.ANCHO = '1120'
        self.ALTO  = '600'
        self.COLOR_FONDO = "#1C2128" 
        self.COLOR_PRIMARIO = "#22272E"
        self.COLOR_FG = "#768390"
        self.COLOR_LINEAS = "#316DCA"
        self.PATH = self.resource_path()
        self.PATH_IMAGE = os.path.join (self.PATH,'images')
        self.PATH_CONFIG = os.path.join (self.PATH,'config')

    def resource_path(self):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path)


class App():

    def __init__(self, master, parent):
        self.PARTENT = parent
        self.MASTER = master
        self.MASTER.grid_columnconfigure(1, weight=1)
        self.MASTER.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self.MASTER,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = ctk.CTkFrame(master=self.MASTER)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = ctk.CTkLabel(master=self.frame_left,
                                              text="Navegación",
                                              text_font=("Roboto Medium", -20),
                                              text_color = "white",
                                              )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = ctk.CTkButton(master=self.frame_left,
                                                text="Actividades",
                                                command=self.button_event)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = ctk.CTkButton(master=self.frame_left,
                                                text="Reporte",
                                                command=self.button_event)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = ctk.CTkButton(master=self.frame_left,
                                                text="Ir a inicio",
                                                command=self.ir_a_inicio)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        """self.switch_1 = ctk.CTkSwitch(master=self.frame_left)
        self.switch_1.grid(row=9, column=0, pady=10, padx=20, sticky="w")"""

        self.switch_2 = ctk.CTkSwitch(master=self.frame_left,
                                                text="Modo oscuro",
                                                command=self.change_mode,
                                                text_color = "white",)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")


        self.frame_right.rowconfigure((0), weight=1)

        today = datetime.date.today()
        mindate = datetime.date(year=2018, month=1, day=21)
        maxdate = today + datetime.timedelta(days=960)
        print(mindate, maxdate)

        cal = Calendar(self.frame_right, font="Cascade 13", selectmode='day', locale='es_ES',
                    mindate=mindate, maxdate=maxdate, disabledforeground='red',
                    cursor="hand2", year=2022, month=5, day=20)
        cal.pack(fill="both", expand=True)

    def button_event(self):
        pass

    def ir_a_inicio (self):
        self.PARTENT.frame_portada.tkraise()

    def change_mode(self):
        if self.switch_2.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


class Portada (Parametros):
    """## Clase que genera una portada"""

    def __init__(self, master) -> None:
        super().__init__()
        self.MASTER = master

        self.MASTER.rowconfigure(0, weight=1)
        self.MASTER.columnconfigure(0, weight=1)

        self.frame_calendario = Frame (self.MASTER, bg = self.COLOR_FONDO)
        self.frame_calendario.grid(row = 0, column = 0, sticky= "nsew")
        
        self.frame_portada = Frame (self.MASTER, bg = self.COLOR_FONDO)
        self.frame_portada.grid( row = 0, column = 0, sticky= "nsew",)
        

        self.frame_up = Frame (self.frame_portada, bg = self.COLOR_PRIMARIO)
        self.frame_down = Frame (self.frame_portada, bg = self.COLOR_PRIMARIO)
        self.frame_up.pack (side = TOP, padx = 10, pady = 10, fill = "both")
        self.frame_down.pack (side = TOP, padx = 10, fill = "both",expand=True)
        self.desplegar_tabla()
        self.buscador()
        #self.abrir()

        self.MASTER.mainloop()
        pass

    def desplegar_tabla (self):
        
        self.tabla_proyectos = sheet.Sheet(self.frame_down,headers= ['Proyecto', 'Descripción', 'Inicio', 'Avance'], data= [[f"Proyecto {i}",f"Este proyecto consiste en tal cosa tal cosa tal cosa",f"202{i}-15-15",f"{i}%",] for i in range (50)],
        show_table = True,
        show_top_left = False,
        show_row_index = True,
        show_header = True,
        show_x_scrollbar = True,
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
        #font = get_font(),
        #header_font = get_heading_font(),
        #popup_menu_font = get_font(),
        align = "w",
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
        self.tabla_proyectos.header_font(newfont = ("Cascade", 16, "normal"))
        self.tabla_proyectos.enable_bindings()
        self.tabla_proyectos.header_align(align = "center", redraw = True)
        self.tabla_proyectos.align_columns(columns = [2,3], align = "center", align_header = True, redraw = True)
        self.tabla_proyectos.column_width(column = 0, width = 150, only_set_if_too_small = False, redraw = True)
        self.tabla_proyectos.column_width(column = 1, width = 600, only_set_if_too_small = False, redraw = True)
        self.tabla_proyectos.column_width(column = 2, width = 130, only_set_if_too_small = False, redraw = True)
        self.tabla_proyectos.column_width(column = 3, width = 120, only_set_if_too_small = False, redraw = True)
        #self.tabla_proyectos.set_all_cell_sizes_to_text(redraw = True)
        self.tabla_proyectos.pack ( fill = "both", padx = 20,pady = 5, expand = True)


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

        self.entry_buscador = ctk.CTkEntry(master=self.frame_buscador_child,text_font=("Cascade", 16),placeholder_text="Buscar proyecto...",width=500,height=40,fg_color=self.COLOR_FONDO)
        self.entry_buscador.pack(padx=20)


        # CREACION DE LOS BOTONES
        self.btn_nuevo = ctk.CTkButton(master=self.frame_botones,text="Nuevo",text_font=("Cascade", 16),width=120,height=40,
                                                border_width=3,corner_radius=8,cursor="hand2")
        self.btn_nuevo.grid(row=0,column=0,pady=15,padx=20)

        self.btn_abrir = ctk.CTkButton(master=self.frame_botones,text="Abrir",text_font=("Cascade", 16),width=120,height=40,
                                                border_width=3,corner_radius=8,cursor="hand2", command = self.abrir)
        self.btn_abrir.grid(row=0, column=1,padx=15)

        self.btn_eliminar = ctk.CTkButton(master=self.frame_botones,text="Eliminar",text_font=("Cascade", 16),width=120,height=40,
                                                border_width=3,corner_radius=8,cursor="hand2")
        self.btn_eliminar.grid(row=0, column=2,padx=13)

    def abrir (self):
        self.frame_calendario.tkraise()
        App (self.frame_calendario, self)


class Main (Parametros):
    """## Clase que genera el frame principal"""

    def __init__(self) -> None:
        super().__init__()
        """### Creación y configuracion de la pagina principal"""


        ctk.set_default_color_theme(os.path.join (self.PATH_CONFIG, "custom_theme.json"))
        #self.RAIZ = Tk("Adminstrador de proyectos", "Administrador de proyectos")
        self.RAIZ = ctk.CTk()
        self.RAIZ.geometry(f'{self.ANCHO}x{self.ALTO}')
        self.RAIZ.resizable(False, False)
        self.RAIZ.title("Administrador de proyectos")
        self.RAIZ.config(bg=self.COLOR_FONDO)
        self.center (self.RAIZ)
        Portada(self.RAIZ)



        self.RAIZ.mainloop()
        pass
        
    
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
    
if __name__ == "__main__":
    Main()

    