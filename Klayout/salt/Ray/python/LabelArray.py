import pya
import numpy as np


class LabelArray(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the LabelArray
    """

    def __init__(self):
        # Important: initialize the super class
        super(LabelArray, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("nLabels", self.TypeInt, "Number of Labels", default=10)
        self.param("text_distance", self.TypeDouble,
                   "Distance between adjacent Labels", default=10.)
        for i in range(self.nLabels):
            self.param(f"Label {i}", self.TypeString)
        
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "LabelArray(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        # x = 0.0
        # y = 0.0
        # for i in range(0, len(self.WL)):
        #     pts = []
        #     pts.append(pya.DPoint(x, y))
        #     x += float(self.WL[i])*self.Wscaling
        #     y += float(self.L)
        #     pts.append(pya.DPoint(x, y))
        #     self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))
        #     label = pya.TextGenerator.default_generator().text("{}".format(int(float(
        #         self.WL[i])*self.labelscaling)), 0.05*self.layout.dbu).move(1000*pts[0].x, 1000*pts[0].y - 1000*self.text_distance)

        #     self.cell.shapes(self.l_layer).insert(label)

        #     x += float(self.spacing)
        #     y -= float(self.L)
        pass
