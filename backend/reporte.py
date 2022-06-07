import os
from arrow import utcnow
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, purple, white, limegreen, gray
from reportlab.pdfgen.canvas import Canvas

# ======================= CLASE reportePDF =========================

class reportePDF(object):
    """Exportar una lista de diccionarios a una tabla en un
       archivo PDF."""
    
    def __init__(self, titulo, cabecera, datos, nombrePDF):
        super(reportePDF, self).__init__()

        self.titulo = titulo
        self.cabecera = cabecera
        self.datos = datos
        self.nombrePDF = nombrePDF

        self.estilos = getSampleStyleSheet()

    @staticmethod
    def _encabezadoPiePagina(canvas, archivoPDF):
        """Guarde el estado de nuestro lienzo para que podamos aprovecharlo"""
        
        canvas.saveState()
        estilos = getSampleStyleSheet()

        alineacion = ParagraphStyle(name="alineacion", alignment=TA_RIGHT,
                                    parent=estilos["Normal"])
 
        # Encabezado
        encabezadoNombre = Paragraph("Project Hub", estilos["Normal"])
        anchura, altura = encabezadoNombre.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoNombre.drawOn(canvas, archivoPDF.leftMargin, 736)

        fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
        fechaReporte = fecha.replace("-", "de")

        encabezadoFecha = Paragraph(fechaReporte, alineacion)
        anchura, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoFecha.drawOn(canvas, archivoPDF.leftMargin, 736)
 
        # Pie de página
        piePagina = Paragraph("Reporte generado por Project Hub.", estilos["Normal"])
        anchura, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
        piePagina.drawOn(canvas, archivoPDF.leftMargin, 15 * mm + (0.2 * inch))
 
        # Suelta el lienzo
        canvas.restoreState()

    def convertirDatos(self):
        """Convertir la lista de diccionarios a una lista de listas para crear
           la tabla PDF."""

        estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,
                                          fontSize=10, textColor=white,
                                          fontName="Helvetica-Bold",
                                          parent=self.estilos["Normal"])

        estiloNormal = self.estilos["Normal"]
        estiloNormal.alignment = TA_LEFT

        claves, nombres = zip(*[[k, n] for k, n in self.cabecera])

        encabezado = [Paragraph(nombre, estiloEncabezado) for nombre in nombres]
        nuevosDatos = [tuple(encabezado)]

        for dato in self.datos:
            nuevosDatos.append([Paragraph(str(dato[clave]), estiloNormal) for clave in claves])
            
        return nuevosDatos
        
    def Exportar(self):
        """Exportar los datos a un archivo PDF."""

        alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13,
                                          leading=10, textColor=gray,
                                          parent=self.estilos["Heading1"])
        
        self.ancho, self.alto = letter

        convertirDatos = self.convertirDatos()
    
        tabla = Table(convertirDatos, colWidths=(self.ancho-100)/len(self.cabecera), hAlign="CENTER")
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0),(-1, 0), gray),
            ("ALIGN", (0, 0),(0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), # Texto centrado y alineado a la izquierda
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black), # Lineas internas
            ("BOX", (0, 0), (-1, -1), 0.25, black), # Linea (Marco) externa
            ]))

        historia = []
        historia.append(Paragraph(self.titulo, alineacionTitulo))
        historia.append(Spacer(1, 0.16 * inch))
        historia.append(tabla)
        
        #f = open("images/gant.jpg", 'rb')

        #historia.append( Image(f))
        #historia.append("images/gant.png")
        
        
        archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Reporte PDF", author="Project Hub")

        
        
        try:
            archivoPDF.build(historia, onFirstPage=self._encabezadoPiePagina,
                             onLaterPages=self._encabezadoPiePagina,
                             canvasmaker=numeracionPaginas)
            

         # +------------------------------------+
            os.startfile("Reporte.pdf")
            return "Reporte generado con éxito."
         # +------------------------------------+
        except PermissionError:
         # +--------------------------------------------+  
            return "Error inesperado: Permiso denegado."
         # +--------------------------------------------+
         

# ================== CLASE numeracionPaginas =======================

class numeracionPaginas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Agregar información de la página a cada página (página x de y)"""
        # Se carga la imagen de reporte tipo gant
        numeroPaginas = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(numeroPaginas)
            #Canvas.showPage(self)
            
        gant = "images/gant.jpg"
        Canvas.drawImage(self ,image = gant, x = 0, y = 0, width=575,preserveAspectRatio=True)
        Canvas.showPage(self)
        Canvas.save(self)
        
        
 
    def draw_page_number(self, conteoPaginas):
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                             "Página {} de {}".format(self._pageNumber, conteoPaginas))        










