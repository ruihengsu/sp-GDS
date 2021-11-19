import pya
import numpy as np

class DotGuide(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the CrossRingLabeled
    """

    def __init__(self):

        # Important: initialize the super class
        super(DotGuide, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))

        self.param("r", self.TypeDouble, "Write radius", default=100.0)
        self.param("n_p", self.TypeInt, "Number of pads", default=8)
        self.param("pw", self.TypeDouble, "Pad width/height", default=2)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "DotGuide(L=%s)" % (str(self.l))

    def produce_impl(self):

        # starting set of coordinates
        x_c = 0 
        y_c = self.r/2 

        angle = 360/self.n_p
       
        pts = [
                pya.DPoint(x_c - 0.5*self.pw, y_c - 0.5*self.pw),
                pya.DPoint(x_c - 0.5*self.pw, y_c + 0.5*self.pw), 
                pya.DPoint(x_c + 0.5*self.pw, y_c + 0.5*self.pw),
                pya.DPoint(x_c + 0.5*self.pw, y_c - 0.5*self.pw),
            ] 
            
        pad = pya.DPolygon(pts)    
        for i in range(self.n_p):
            tt = pya.DCplxTrans(1,  i*angle, False, 0,0)            
            self.cell.shapes(self.l_layer).insert(tt* pad)
