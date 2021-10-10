import pya
import numpy as np

class EtchTest_Circ(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the EtchTest_Circ
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Circ, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("SR", self.TypeDouble, "Starting Radius", default=1000.)
        self.param("dR", self.TypeDouble, "Dr", default=50.)
        self.param("MinR", self.TypeDouble, "Minimum radius", default=5.)
        self.param("spacing", self.TypeDouble,
                   "Spacing between structures", default=100.)
        self.param("res", self.TypeInt,
                   "Resolution", default=100.)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Circ(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout

        radians = np.linspace(0, 2*np.pi, self.res, endpoint=False)

        starting_radius = self.SR
        offset = 0
        while starting_radius > self.MinR:
            pts = []
            for theta in radians:
                x = starting_radius*np.cos(theta) + offset
                y = starting_radius*np.sin(theta)
                pts.append(pya.DPoint(x, y))
            self.cell.shapes(self.l_layer).insert(pya.DPolygon(pts))

            offset += self.spacing
            starting_radius -= self.dR
