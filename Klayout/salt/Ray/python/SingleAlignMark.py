import pya
import numpy as np

class SingleAlignMark(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the SingleAlignMark
    """

    def __init__(self):

        # Important: initialize the super class
        super(SingleAlignMark, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))

        self.param("width", self.TypeDouble, "Rectangle width", default=300.0)
        self.param("length", self.TypeDouble,
                   "Rectangle length", default=300.0)

        self.param("cwidth", self.TypeDouble, "Cross width", default=200.0)
        self.param("clength", self.TypeDouble, "Cross length", default=200.0)
        self.param("cthick", self.TypeDouble, "Cross thickness", default=10.0)
    
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "SingleAlignMark(L=%s)" % (str(self.l))

    def produce_impl(self):
        lower_left = pya.DPoint(-self.width/2, -self.length/2)
        upper_right = pya.DPoint(self.width/2, self.length/2)
        square = pya.DBox(lower_left, upper_right)

        l0 = pya.Region()
        l0.insert(square)

        c1 = pya.DPoint(-self.cwidth/2, 0)*scaling_factor
        c2 = pya.DPoint(self.cwidth/2, 0)*scaling_factor
        p1 = pya.DPath([c1, c2], self.cthick)

        l1 = pya.Region()
        l1.insert(p1)

        c3 = pya.DPoint(0, -self.clength/2)
        c4 = pya.DPoint(0, self.clength/2)
        p2 = pya.DPath([c3, c4], self.cthick)

        l2 = pya.Region()
        l2.insert(p2)
        
        

        result = l0 - l1 - l2
        self.cell.shapes(self.l_layer).insert(result)