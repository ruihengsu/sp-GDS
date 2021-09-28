import pya
import numpy as np

class RCLine(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the RCLine
    """

    def __init__(self):

        # Important: initialize the super class
        super(RCLine, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("line_W", self.TypeDouble, "Line width", default=50.0)
        self.param("line_L", self.TypeDouble, "Line length", default=500.0)
        self.param("pad_W", self.TypeDouble, "Bond pad width", default=300.0)
        self.param("pad_L", self.TypeDouble, "Bond pad length", default=300.0)
        self.param("text_distance", self.TypeDouble,
                   "Offset parameter between the bottom edge of the RC line, and the label", default=60.0)
        self.param("text_scale", self.TypeDouble,
                   "Scaling parameter for the text size", default=0.02)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "RCLine(L=%s)" % (str(self.l))

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        # compute the Serpentine: generate a list of spine points for the path and then
        # create the path

        squares = self.line_L/self.line_W

        pts = []
        x = -self.pad_W/2
        y = -self.pad_L - self.line_L/2

        pts.append(pya.DPoint(x, y))

        label = pya.TextGenerator.default_generator().text("{}".format(squares), self.text_scale *
                                                           self.layout.dbu).move(1000*pts[0].x, 1000*pts[0].y - 1000*self.text_distance)
        self.cell.shapes(self.l_layer).insert(label)

        x = self.pad_W/2
        y = -self.line_L/2
        pts.append(pya.DPoint(x, y))

        self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))

        pts = []
        x = 0
        y = -self.line_L/2
        pts.append(pya.DPoint(x, y))

        x = 0
        y = self.line_L/2
        pts.append(pya.DPoint(x, y))
        self.cell.shapes(self.l_layer).insert(pya.DPath(pts, self.line_W))

        pts = []
        x = -self.pad_W/2
        y = self.line_L/2
        pts.append(pya.DPoint(x, y))

        x = self.pad_W/2
        y = self.line_L/2 + self.pad_L
        pts.append(pya.DPoint(x, y))

        self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))