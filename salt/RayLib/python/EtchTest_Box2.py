import pya
import numpy as np

class EtchTest_Box2(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the EtchTest_Box2
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Box2, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("LL", self.TypeList, "Length List", default=[
                   1000., 1000., 1000., 1000., 1000., 1000., 1000., 1000.])
        self.param("WL", self.TypeList, "Width List",
                   default=[100, 50., 30, 20, 10,  9, 8, 7, ])
        self.param("spacing", self.TypeList,
                   "Spacing between structures", default=[0, 50., 50, 50, 50,  50, 50, 50, ])

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Box2(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout

        assert (len(self.LL) == len(self.WL) == len(self.spacing))

        x = 0.0
        y = 0.0
        for i in range(0, len(self.LL)):
            pts = []

            x += float(self.spacing[i])
            pts.append(pya.DPoint(x, y))
            x += float(self.WL[i])
            y += float(self.LL[i])
            pts.append(pya.DPoint(x, y))
            self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))

            y -= float(self.LL[i])
            # x += float(self.spacing[i])

