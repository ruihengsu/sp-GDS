import pya
import numpy as np

class BoundingBox(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the BoundingBox
    """

    def __init__(self):

        # Important: initialize the super class
        super(BoundingBox, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("OL", self.TypeDouble, "Outer height", default=5000.,)
        self.param("OW", self.TypeDouble, "Outer width", default=5000.,)
        self.param("IL", self.TypeDouble, "DL", default=100.,)
        self.param("IW", self.TypeDouble, "DW", default=100.,)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "BoundingBox(Layer=%s)"

    def produce_impl(self):
        scaling_factor = int(1/self.layout.dbu)
    
        lower_left = pya.DPoint(-self.OW/2, -self.OL/2)*scaling_factor
        upper_right = pya.DPoint(self.OW/2, self.OL/2)*scaling_factor
        rect = pya.DBox(lower_left, upper_right)

        l0 = pya.Region()
        l0.insert(rect)

      
        lower_left = pya.DPoint(-self.OW/2+self.IW, -self.OL/2+self.IL)*scaling_factor
        upper_right = pya.DPoint(self.OW/2-self.IW, self.OL/2 - self.IL)*scaling_factor
        rect = pya.DBox(lower_left, upper_right)

        l1 = pya.Region()
        l1.insert(rect)

        result = l0 - l1
        self.cell.shapes(self.l_layer).insert(result)