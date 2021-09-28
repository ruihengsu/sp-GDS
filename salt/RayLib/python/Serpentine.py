import pya
import math
import numpy as np


class Serpentine(pya.PCellDeclarationHelper):
    """
    The PCell declaration for Serpentine
    """

    def __init__(self):

        # Important: initialize the super class
        super(Serpentine, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("n", self.TypeInt,
                   "Number of points per full turn", default=5)
        self.param("w", self.TypeDouble, "The width", default=1.0)
        self.param("u", self.TypeDouble, "One turn's pitch", default=2.0)
        self.param("s", self.TypeDouble, "The turn's length", default=20.0)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "Serpentine(L=%s,S=%.12g,U=%.12g)" % (str(self.l), self.s, self.u)

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        # compute the Serpentine: generate a list of spine points for the path and then
        # create the path

        pts = []

        x = 0.0
        y = 0.0

        for i in range(0, self.n):
            pts.append(pya.DPoint(x, y))
            x += self.u
            pts.append(pya.DPoint(x, y))
            if (i % 2) == 0:
                y += self.s
            else:
                y -= self.s
            pts.append(pya.DPoint(x, y))

        # One last point to move to the end location
        x += self.u
        pts.append(pya.DPoint(x, y))

        # create the shape
        self.cell.shapes(self.l_layer).insert(pya.DPath(pts, self.w))