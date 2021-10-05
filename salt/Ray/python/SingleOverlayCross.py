import pya
import numpy as np

class SingleOverlayCross(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the SingleAlignMark
    """

    def __init__(self):

        # Important: initialize the super class
        super(SingleOverlayCross, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        
        self.param("cwidth", self.TypeDouble, "Cross width", default=200.0)
        self.param("clength", self.TypeDouble, "Cross length", default=200.0)
        self.param("cthick", self.TypeDouble, "Cross thickness", default=10.0)
        
        self.param("othick", self.TypeDouble, "Overlay thickness", default=10.0)
        self.param("olength", self.TypeDouble, "Overlay length", default=80.0)
        self.param("opitch", self.TypeDouble, "Overlay pitch", default=15.0)
        self.param("oN", self.TypeInt, "Number of overlay marks", default=4)
        
        self.param("oxp", self.TypeBoolean, "Enable +x overlay marks", default=True)
        self.param("oxn", self.TypeBoolean, "Enable -x overlay marks", default=True)
        self.param("oyp", self.TypeBoolean, "Enable +y overlay marks", default=True)
        self.param("oyn", self.TypeBoolean, "Enable -y overlay marks", default=True)
        
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "SingleOverlayCross(L=%s)" % (str(self.l))

    def produce_impl(self):
        
        scaling_factor = int(1/self.layout.dbu)
        
        c1 = pya.DPoint(-self.cwidth/2, 0)*scaling_factor
        c2 = pya.DPoint(self.cwidth/2, 0)*scaling_factor
        p1 = pya.DPath([c1, c2], self.cthick*scaling_factor)

        l1 = pya.Region()
        l1.insert(p1)

        c3 = pya.DPoint(0, -self.clength/2)*scaling_factor
        c4 = pya.DPoint(0, self.clength/2)*scaling_factor
        p2 = pya.DPath([c3, c4], self.cthick*scaling_factor)

        l2 = pya.Region()
        l2.insert(p2)
        
        result = l1 + l2
        
        for i in range(self.oN):
        
            if self.oxn:
                c5 = pya.DPoint(c1.x + i*self.opitch*scaling_factor,  
                                        scaling_factor*self.olength/2)   
                c6 = pya.DPoint(c1.x + i*self.opitch*scaling_factor, 
                                       -scaling_factor*self.olength/2)
                p3 = pya.DPath([c5, c6], self.othick*scaling_factor)
                l3 = pya.Region()
                l3.insert(p3)
                result += l3
                
            if self.oxp:
                c7 = pya.DPoint(c2.x - i*self.opitch*scaling_factor,  
                                        scaling_factor*self.olength/2)   
                c8 = pya.DPoint(c2.x - i*self.opitch*scaling_factor,  
                                       -scaling_factor*self.olength/2)
                p4 = pya.DPath([c7, c8], self.othick*scaling_factor)
                l4 = pya.Region()
                l4.insert(p4)
                result += l4
            
            if self.oyn:
                c9 = pya.DPoint(scaling_factor*self.olength/2,  
                                        c3.y + i *self.opitch*scaling_factor)   
                c10 = pya.DPoint(-scaling_factor*self.olength/2,  
                                         c3.y + i *self.opitch*scaling_factor)   
                p5 = pya.DPath([c9, c10], self.othick*scaling_factor)
                l5 = pya.Region()
                l5.insert(p5)
                result += l5
            
            if self.oyp:
                c11 = pya.DPoint(scaling_factor*self.olength/2, 
                                          c4.y - i *self.opitch*scaling_factor)   
                c12 = pya.DPoint(-scaling_factor*self.olength/2, 
                                          c4.y - i *self.opitch*scaling_factor)
                p6 = pya.DPath([c11, c12], self.othick*scaling_factor)
                l6 = pya.Region()
                l6.insert(p6)
                result += l6
                
        self.cell.shapes(self.l_layer).insert(result)