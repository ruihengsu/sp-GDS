import pya
import numpy as np


class InnerLeads(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the CrossRingLabeled
    """

    def __init__(self):

        # Important: initialize the super class
        super(InnerLeads, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))

        self.param("w1", self.TypeDouble, "Width 1", default=2.0)
        self.param("w2", self.TypeDouble, "Width 2", default=1.0)
        self.param("length", self.TypeDouble, "length", default=5.0)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "InnerLeads(L=%s)" % (str(self.l))

    def produce_impl(self):

        pts = [
            pya.DPoint(-0.5*self.w1, self.length),
            pya.DPoint(0.5*self.w1, self.length),
            pya.DPoint(0.5*self.w2, 0),
            pya.DPoint(-0.5*self.w2, 0),
        ]

        pad = pya.DPolygon(pts,)
        # for i in range(self.n_p):
        #    tt = pya.DCplxTrans(1,  i*angle, False, 0,0)
        self.cell.shapes(self.l_layer).insert(pad)
