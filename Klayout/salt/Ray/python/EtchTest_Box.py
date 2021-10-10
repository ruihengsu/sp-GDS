import pya
import numpy as np

class EtchTest_Box(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the EtchTest_Box
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Box, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("SL", self.TypeDouble, "Starting Length", default=1000.)
        self.param("SW", self.TypeDouble, "Starting Width", default=1000.)
        self.param("dW", self.TypeDouble, "Dw", default=50.)
        self.param("dL", self.TypeDouble, "Dl", default=50.)
        self.param("MinL", self.TypeDouble, "Minimum Length", default=5.)
        self.param("MinW", self.TypeDouble, "Minimum Width", default=5.)
        self.param("spacing", self.TypeDouble,
                   "Spacing between structures", default=100.)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Box(Layer=%s,Starting Length=%.12g, Starting Width=%.12g, Dw=%.12g, Dl=%.12g, Minimum Length=%.12g, Minimum Width=%.12g, Spacing=%.12g)" % (str(self.l), self.SL, self.SW, self.dW, self.dL, self.MinL, self.MinW, self.spacing)

    def produce_impl(self):
        # This is the main part of the implementation: create the layout

        x = 0.0
        y = 0.0

        starting_width = self.SW
        starting_length = self.SL

        while starting_width > self.MinW and starting_length > self.MinL:

            pts = []
            pts.append(pya.DPoint(x, y))
            x += starting_width
            y += starting_length
            pts.append(pya.DPoint(x, y))
            print(pts)
            self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))

            y -= starting_length
            x += self.spacing

            starting_width -= self.dW
            starting_length -= self.dL
