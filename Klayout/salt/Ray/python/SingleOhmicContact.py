import pya
import numpy as np

class SingleOhmicContact (pya.PCellDeclarationHelper):
    """
    The PCell declaration for the SingleOhmicContact
    """

    def __init__(self):

        # Important: initialize the super class
        super(SingleOhmicContact, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("X", self.TypeDouble, "X", default=200.)
        self.param("Y", self.TypeDouble, "Y", default=200.)
        self.param("A", self.TypeInt, "Amplitude", default=1)
        self.param("H", self.TypeInt, "Harmonic", default=1)
        self.param("R", self.TypeInt, "Resolution", default=2)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "SingleOhmicContact(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        pts = []

        edges_x = np.linspace(-1, 1, num=self.R, endpoint=True)
        edges_y = self.A*np.sin(self.H*2*np.pi*edges_x)

        print(edges_x)
        print(edges_y)

        edges_x1 = edges_x*self.X/2
        edges_y1 = -1*edges_y - self.Y/2
        print(edges_x1)
        print(edges_y1)

        for p in zip(edges_x1, edges_y1):
            pts.append(pya.DPoint(p[0], p[1]))

        edges_x2 = edges_y + self.X/2
        edges_y2 = edges_x*self.Y/2
        print(edges_x2)
        print(edges_y2)

        for p in zip(edges_x2, edges_y2):
            pts.append(pya.DPoint(p[0], p[1]))

        edges_x3 = -1*edges_x*self.X/2
        edges_y3 = edges_y + self.Y/2
        print(edges_x3)
        print(edges_y3)

        for p in zip(edges_x3, edges_y3):
            pts.append(pya.DPoint(p[0], p[1]))

        edges_x4 = -1*edges_y - self.X/2
        edges_y4 = -1*edges_x*self.Y/2
        print(edges_x4)
        print(edges_y4)

        for p in zip(edges_x4, edges_y4):
            pts.append(pya.DPoint(p[0], p[1]))

        self.cell.shapes(self.l_layer).insert(pya.DPolygon(pts))