import pya
import numpy as np

class RCLineArray(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the RCLineArray
    """

    def __init__(self):

        # Important: initialize the super class
        super(RCLineArray, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("line_W", self.TypeDouble, "Line width", default=50.0)
        self.param("line_L", self.TypeDouble, "Line length", default=500.0)
        self.param("pad_W", self.TypeDouble, "Bond pad width", default=300.0)
        self.param("pad_L", self.TypeDouble, "Bond pad length", default=300.0)
        
        self.param("rows", self.TypeInt, "Number of rows", default=2)
        self.param("columns", self.TypeInt, "Number of columns", default=2)
        self.param("row_step", self.TypeDouble, "Row step", default=300.0)
        self.param("col_step", self.TypeDouble, "Col step", default=300.0)
        
        self.param("text_distance", self.TypeDouble,
                   "Offset parameter between the bottom edge of the RC line, and the label", default=60.0)
        self.param("text_scale", self.TypeDouble,
                   "Scaling parameter for the text size", default=0.02)
            
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "RCLineArray(L=%s)" % (str(self.l))

    def produce_impl(self):
        
        x = np.linspace(0, self.rows, endpoint=False,
                        num=self.rows, dtype=int)*self.row_step
        y = np.linspace(0, self.columns, endpoint=False,
                        num=self.columns,)*self.col_step

        XX, YY = np.meshgrid(x, y, indexing='ij')

        grid = np.zeros((self.rows, self.columns), dtype='i,i')

        for i in range(0, self.rows):
            for j in range(0, self.columns):
                grid[i, j] = (XX[i, j], YY[i, j])
                print(grid[i, j])

        for i, p in enumerate(grid.flatten()):
            c_x = float(p[0])
            c_y = float(p[1])
            
            pts = []
            x = c_x-self.pad_W/2
            y = c_y-self.pad_L - self.line_L/2
    
            pts.append(pya.DPoint(x, y))
    
            label = pya.TextGenerator.default_generator().text("{}".format(i + 1), self.text_scale *
                                                               self.layout.dbu).move(1000*pts[0].x, 1000*pts[0].y - 1000*self.text_distance)
            self.cell.shapes(self.l_layer).insert(label)
    
            x = c_x + self.pad_W/2
            y = c_y-self.line_L/2
            pts.append(pya.DPoint(x, y))
    
            self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))
    
            pts = []
            x = c_x
            y = c_y-self.line_L/2
            pts.append(pya.DPoint(x, y))
    
            x = c_x
            y = c_y+self.line_L/2
            pts.append(pya.DPoint(x, y))
            self.cell.shapes(self.l_layer).insert(pya.DPath(pts, self.line_W))
    
            pts = []
            x = c_x-self.pad_W/2
            y = c_y+self.line_L/2
            pts.append(pya.DPoint(x, y))
    
            x = c_x+self.pad_W/2
            y = c_y+ self.line_L/2 + self.pad_L
            pts.append(pya.DPoint(x, y))
    
            self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))