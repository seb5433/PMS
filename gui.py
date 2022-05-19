# GUI del administrador de proyectos

from tkinter import *

class Portada ():
    """## Clase que genera una portada"""

    def __init__(self) -> None:
        self.RAIZ = Tk("Adminstrador de proyectos", "Administrador de proyectos")
        self.RAIZ.mainloop()
        pass
    
if __name__ == "__main__":
    Portada()

    