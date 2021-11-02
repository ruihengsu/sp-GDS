import pya
import numpy as np

class CrossRingLabeled(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the CrossRingLabeled
    """

    def __init__(self):

        # Important: initialize the super class
        super(CrossRingLabeled, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))

        self.param("cwidth", self.TypeDouble, "Cross width", default=120.0)
        self.param("clength", self.TypeDouble, "Cross length", default=120.0)
        self.param("cthick", self.TypeDouble, "Cross thickness", default=8.0)

        self.param("rows", self.TypeInt, "Number of rows", default=2)
        self.param("columns", self.TypeInt, "Number of columns", default=2)

        self.param("row_step", self.TypeDouble, "Row step", default=300.0)
        self.param("col_step", self.TypeDouble, "Col step", default=300.0)
        
        self.param("width", self.TypeDouble, "Text x-Position Parameter", default=180.0)
        
        self.param("text_distance", self.TypeDouble,
                   "Text distance", default=75.0)
                   
        self.param("text_scale", self.TypeDouble,
                   "Text scaling factor", default=0.04)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "CrossRingLabeled(L=%s)" % (str(self.l))

    def produce_impl(self):

        scaling_factor = int(1/self.layout.dbu)
        print(scaling_factor)
        x = np.linspace(0, self.rows, endpoint=False,
                        num=self.rows, dtype=int)*self.row_step
        y = np.linspace(0, self.columns, endpoint=False,
                        num=self.columns,)*self.col_step
        
        for py in [y[0], y[-1]]:
          for px in x: 
          
            c_x = px 
            c_y = py
            
            c1 = pya.DPoint(c_x-self.cwidth/2.0, c_y)*scaling_factor
            c2 = pya.DPoint(c_x+self.cwidth/2, c_y)*scaling_factor
            p1 = pya.DPath([c1, c2], self.cthick*scaling_factor)
  
            l1 = pya.Region()
            l1.insert(p1)
  
            c3 = pya.DPoint(c_x, c_y-self.clength/2)*scaling_factor
            c4 = pya.DPoint(c_x, c_y+self.clength/2)*scaling_factor
            p2 = pya.DPath([c3, c4], self.cthick*scaling_factor)
  
            l2 = pya.Region()
            l2.insert(p2)
  
            label = pya.TextGenerator.default_generator().text("{},{}".format(int(p[0]-x.max()/2), 
                                                                              int(p[1]-y.max()/2)), 
                                                               self.text_scale*self.layout.dbu).move(1000*(c_x-self.width/2 + self.width/40), 
                                                                                                     1000*c_y - 1000*self.text_distance)
                                                                                                       
            result = l1 + l2 + label
            self.cell.shapes(self.l_layer).insert(result)
        
        for px in [x[0], x[-1]]:
          for py in y: 
          
            c_x = px 
            c_y = py
            
            c1 = pya.DPoint(c_x-self.cwidth/2.0, c_y)*scaling_factor
            c2 = pya.DPoint(c_x+self.cwidth/2, c_y)*scaling_factor
            p1 = pya.DPath([c1, c2], self.cthick*scaling_factor)
  
            l1 = pya.Region()
            l1.insert(p1)
  
            c3 = pya.DPoint(c_x, c_y-self.clength/2)*scaling_factor
            c4 = pya.DPoint(c_x, c_y+self.clength/2)*scaling_factor
            p2 = pya.DPath([c3, c4], self.cthick*scaling_factor)
  
            l2 = pya.Region()
            l2.insert(p2)
  
            label = pya.TextGenerator.default_generator().text("{},{}".format(int(p[0]-x.max()/2), 
                                                                              int(p[1]-y.max()/2)), 
                                                               self.text_scale*self.layout.dbu).move(1000*(c_x-self.width/2 + self.width/40), 
                                                                                                     1000*c_y - 1000*self.text_distance)
                                                                                                       
            result = l1 + l2 + label
            self.cell.shapes(self.l_layer).insert(result)

        

