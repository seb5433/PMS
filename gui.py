# GUI del administrador de proyectos

from tkinter import *
import tksheet as sheet
import customtkinter
import os
import sys

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

    def resource_path(self):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path)


class Portada (Parametros):
    """## Clase que genera una portada"""

    def __init__(self, master) -> None:
        super().__init__()
        self.MASTER = master

        self.frame_up = Frame (self.MASTER, bg = self.COLOR_PRIMARIO)
        self.frame_down = Frame (self.MASTER, bg = self.COLOR_PRIMARIO)
        self.frame_up.pack (side = TOP, padx = 10, pady = 10, fill = "both")
        self.frame_down.pack (side = TOP, padx = 10, fill = "both",expand=True)
        self.desplegar_tabla()
        self.buscador()

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
        self.lbl_buscar_image = PhotoImage(file=os.path.join( self.PATH_IMAGE,"buscar2.png"))

        # CREACION DE FRAMES

        self.frame_buscador_child = Frame(self.frame_up, bg=self.COLOR_PRIMARIO)
        self.frame_buscador_child.grid(row=0, column=0)

        self.frame_espacio_vacio = Frame (self.frame_up,bg=self.COLOR_PRIMARIO)
        self.frame_espacio_vacio.grid(row=0,column=1,padx=20)

        self.frame_botones = Frame (self.frame_up,bg=self.COLOR_PRIMARIO)
        self.frame_botones.grid(row=0,column=2,columnspan=3,rowspan=2)


        # CREACION DEL ENTRY
        self.text_search = StringVar()

        self.entry_buscador = Entry(self.frame_buscador_child, textvariable=self.text_search, width=42, font=("Arial", 16))
        self.entry_buscador.grid(row=1,column=0, padx=3, sticky=N)


        # CREACION DEL LABEL BUSCAR PROYECTO IMAGEN
        self.lbl_buscar = Label(self.frame_buscador_child, bg=self.COLOR_PRIMARIO, image=self.lbl_buscar_image, relief="flat")
        self.lbl_buscar.grid(row=0, column=0, sticky=W)

        # CREACION DE LABELS VACIO 
        self.espacio_vacio_1= Label (self.frame_botones,relief="flat", bg=self.COLOR_PRIMARIO) 
        self.espacio_vacio_1.grid(row=0,column=0)

        self.espacio_vacio_2 = Label (self.frame_espacio_vacio,relief="flat", bg=self.COLOR_PRIMARIO) 
        self.espacio_vacio_2.grid(row=0,column=0)


        # CREACION DE LAS IMAGENES DE LOS BOTONES        
        self.btn_nuevo_image = PhotoImage(file=os.path.join( self.PATH_IMAGE,"nuevo3.png"))
        self.btn_abrir_image = PhotoImage(file=os.path.join( self.PATH_IMAGE,"abrir3.png"))
        self.btn_eliminar_image = PhotoImage(file=os.path.join( self.PATH_IMAGE,"eliminar.png"))

        # CREACION DE LOS BOTONES
        self.btn_nuevo = Button(self.frame_botones, bg=self.COLOR_PRIMARIO, image=self.btn_nuevo_image, relief="flat", cursor="hand2")
        self.btn_nuevo.grid(row=1,column=0,pady=15,padx=10)

        self.btn_abrir = Button(self.frame_botones, bg=self.COLOR_PRIMARIO, image=self.btn_abrir_image, relief="flat", cursor="hand2")
        self.btn_abrir.grid(row=1, column=1,padx=10)

        self.btn_eliminar = Button(self.frame_botones, bg=self.COLOR_PRIMARIO, image=self.btn_eliminar_image, relief="flat", cursor="hand2")
        self.btn_eliminar.grid(row=1, column=2,padx=8)

class Main (Parametros):
    """## Clase que genera el frame principal"""

    def __init__(self) -> None:
        super().__init__()
        """### Creación y configuracion de la pagina principal"""


        customtkinter.set_default_color_theme("blue")
        #self.RAIZ = Tk("Adminstrador de proyectos", "Administrador de proyectos")
        self.RAIZ = customtkinter.CTk()
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

    