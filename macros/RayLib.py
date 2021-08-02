import pya
import math
import numpy as np
"""
This Code implements a Serpentine PCell 

It will generate a path starting from 0,0 and produce a serpentine this
way:

    +->+  +->    ^ 
    ^  |  ^      |
    |  |  |      |
    |  |  |      | s
    |  |  |      |
    |  |  |      |
    |  V  |      |
 +->+  +->+      V

    <-> u

The parameters are:
- l: the layer to use
- w: the width of the path
- n: the number of vertical paths
- u: see drawing above
- s: see drawing above

NOTE: using negative angles makes the Serpentine turn the other way

"""


class Serpentine(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Serpentine
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


class Meander(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Meander
    """

    def __init__(self):

        # Important: initialize the super class
        super(Meander, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("n", self.TypeInt, "Number of turns", default=9)
        self.param("w", self.TypeDouble, "Width of meander line", default=50.)
        self.param("u", self.TypeDouble, "Pitch", default=180.0)
        self.param("s", self.TypeDouble,
                   "Length of meander line", default=1000.0)
        self.param("t", self.TypeDouble,
                   "Additional Thickness", default=1000.0)
        self.param("bl", self.TypeDouble, "Bond line length", default=1000.0)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "Meander(Layer=%s,Length=%.12g,Pitch=%.12g,Width=%.12g)" % (str(self.l), self.s, self.u, self.w)

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        # compute the Serpentine: generate a list of spine points for the path and then
        # create the path
        print("NEW")
        pts = []

        box_pts = dict()

        x = 0.0
        y = self.s/2.

        pts.append(pya.DPoint(x, y))
        y -= self.s/2.

        for i in range(0, self.n):
            print(x, y)
            pts.append(pya.DPoint(x, y))
            x += self.u
            print(x, y)
            pts.append(pya.DPoint(x, y))

            if (i % 2) == 0:
                y += self.s
            else:
                y -= self.s
            print(x, y)
            pts.append(pya.DPoint(x, y))

            if (i % 2) == 0:
                box_pts[i] = (pya.DPoint(pts[-2].x + self.w/2, pts[-2].y - self.w/2),
                              pya.DPoint(pts[-3].x - self.w/2, pts[-2].y - self.t - self.w/2))

            else:
                box_pts[i] = (pya.DPoint(pts[-2].x + self.w/2, pts[-2].y + self.w/2),
                              pya.DPoint(pts[-3].x - self.w/2, pts[-2].y + self.t + self.w/2))

        # One last point to move to the end location
        x += self.u
        print("LAST")
        print(x, y)
        pts.append(pya.DPoint(x, y))

        if ((i+1) % 2) != 0:
            box_pts[i+1] = (pya.DPoint(pts[-1].x + self.w/2, pts[-1].y + self.w/2),
                            pya.DPoint(pts[-2].x - self.w/2, pts[-1].y + self.t + self.w/2))
        else:
            box_pts[i+1] = (pya.DPoint(pts[-1].x + self.w/2, pts[-1].y - self.w/2),
                            pya.DPoint(pts[-2].x - self.w/2, pts[-1].y - self.t - self.w/2))

        if (i % 2) == 0:
            y -= self.s/2
        else:
            y = self.s/2
        print(x, y)
        pts.append(pya.DPoint(x, y))

        for k in box_pts.keys():
            print(box_pts[k][0].x, box_pts[k][0].y,
                  box_pts[k][1].x, box_pts[k][1].y)

        # create the shape
        self.cell.shapes(self.l_layer).insert(pya.DPath(pts, self.w))

        for k in box_pts.keys():
            self.cell.shapes(self.l_layer).insert(
                pya.DBox(box_pts[k][0], box_pts[k][1]))

        bond_line_right_pts = []
        bond_line_right_pts.append(pya.DPoint(pts[0].x + self.w/2, pts[0].y))
        bond_line_right_pts.append(pya.DPoint(
            pts[0].x - self.bl - self.w/2, pts[0].y))

        self.cell.shapes(self.l_layer).insert(
            pya.DPath(bond_line_right_pts, self.w))

        bond_line_left_pts = []
        bond_line_left_pts.append(pya.DPoint(pts[-1].x - self.w/2, pts[-1].y))
        bond_line_left_pts.append(pya.DPoint(
            pts[-1].x + self.bl + self.w/2, pts[-1].y))

        self.cell.shapes(self.l_layer).insert(
            pya.DPath(bond_line_left_pts, self.w))


class EtchTest_Box(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Meander
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Box, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("SL", self.TypeDouble, "Starting Length", default=1000.)
        self.param("SW", self.TypeDouble, "Starting Width", default=1000.)
        self.param("dW", self.TypeDouble, "Dw", default=50.)
        self.param("dL", self.TypeDouble, "Dl", default=50.)
        self.param("MinL", self.TypeDouble, "Minimum Length", default=5.)
        self.param("MinW", self.TypeDouble, "Minimum Width", default=5.)
        self.param("spacing", self.TypeDouble,
                   "Spacing between structures", default=100.)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Box(Layer=%s,Starting Length=%.12g, Starting Width=%.12g, Dw=%.12g, Dl=%.12g, Minimum Length=%.12g, Minimum Width=%.12g, Spacing=%.12g)" % (str(self.l), self.SL, self.SW, self.dW, self.dL, self.MinL, self.MinW, self.spacing)

    def produce_impl(self):
        # This is the main part of the implementation: create the layout

        x = 0.0
        y = 0.0

        starting_width = self.SW
        starting_length = self.SL

        while starting_width > self.MinW and starting_length > self.MinL:

            pts = []
            pts.append(pya.DPoint(x, y))
            x += starting_width
            y += starting_length
            pts.append(pya.DPoint(x, y))
            print(pts)
            self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))

            y -= starting_length
            x += self.spacing

            starting_width -= self.dW
            starting_length -= self.dL

class EtchTest_Box2(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Meander
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Box2, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("LL", self.TypeList, "Length List", default=[1000., 1000., 1000., 1000., 1000., 1000., 1000., 1000.])
        self.param("WL", self.TypeList, "Width List", default=[100, 50., 30, 20, 10,  9, 8, 7, ])
        self.param("spacing", self.TypeList,
                   "Spacing between structures", default=[0, 50., 50, 50, 50,  50, 50, 50, ])

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Box2(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        
        assert (len(self.LL) == len(self.WL) == len(self.spacing))
        
        x = 0.0
        y = 0.0
        for i in range(0, len(self.LL)):
                pts = []
            
                x += float(self.spacing[i])
                pts.append(pya.DPoint(x, y))
                x += float(self.WL[i])
                y += float(self.LL[i])
                pts.append(pya.DPoint(x, y))
                self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))
    
                y -=  float(self.LL[i])
                # x += float(self.spacing[i])

class EtchTest_Box3(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Meander
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Box3, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("L", self.TypeDouble, "Length", default=1000)
        self.param("WL", self.TypeList, "Width List", default=(np.linspace(1000, 1, 101, dtype=int)).tolist())
        self.param("text_distance", self.TypeDouble,
                   "Distance between the structure and the bottom of the text", default=10.)
        self.param("spacing", self.TypeDouble,
                   "Spacing between structures", default=50.)
        self.param("Wscaling", self.TypeDouble,
                   "Actual width is equal to what is specified, times this scaling parameter", default=1/1000.)
        self.param("labelscaling", self.TypeDouble,
                   "Changes units of labels", default=1000)
        # print((np.linspace(1000, 1, 11, dtype=int)).tolist())
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Box3(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        
        lib = pya.Library.library_by_name("Basic")
        if lib == None:
          raise Exception("Unknown lib 'Basic'")
        pcell_decl = lib.layout().pcell_declaration("TEXT");
        if pcell_decl == None:
          raise Exception("Unknown PCell 'TEXT'")
          
        x = 0.0
        y = 0.0
        for i in range(0, len(self.WL)):
                pts = []
                pts.append(pya.DPoint(x, y))
                x += float(self.WL[i])*self.Wscaling
                y += float(self.L)
                pts.append(pya.DPoint(x, y))
                self.cell.shapes(self.l_layer).insert(pya.DBox(pts[0], pts[1]))
                label = pya.TextGenerator.default_generator().text("{}".format(int(float(self.WL[i])*self.labelscaling)), 0.05*self.layout.dbu).move(1000*pts[0].x, 1000*pts[0].y - 1000*self.text_distance)
                
                self.cell.shapes(self.l_layer).insert(label)
                
                x += float(self.spacing)
                y -=  float(self.L)
                

class EtchTest_Circ(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Meander
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Circ, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("SR", self.TypeDouble, "Starting Radius", default=1000.)
        self.param("dR", self.TypeDouble, "Dr", default=50.)
        self.param("MinR", self.TypeDouble, "Minimum radius", default=5.)
        self.param("spacing", self.TypeDouble,
                   "Spacing between structures", default=100.)
        self.param("res", self.TypeInt,
                   "Resolution", default=100.)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Circ(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout

        radians = np.linspace(0, 2*np.pi, self.res, endpoint = False)

        starting_radius = self.SR
        offset = 0
        while starting_radius > self.MinR:
            pts = []
            for theta in radians:
                x = starting_radius*np.cos(theta) + offset
                y = starting_radius*np.sin(theta)
                pts.append(pya.DPoint(x, y))
            self.cell.shapes(self.l_layer).insert(pya.DPolygon(pts))
            
            offset += self.spacing
            starting_radius -= self.dR


class EtchTest_Circ2(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Meander
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Circ2, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("RL", self.TypeList , "Radius list", default=[50,40,30,20,10])
        self.param("SL", self.TypeList,
                   "Spacing List", default=[100,100,100,30,30])
        self.param("res", self.TypeInt,
                   "Resolution", default=100.)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Circ2(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        assert len(self.RL) == len(self.SL)
        radians = np.linspace(0, 2*np.pi, self.res, endpoint = False)
        
        offset = 0
        for i, R in enumerate(self.RL):
            offset +=  float(self.SL[i])
            print(R)
            pts = []
            for theta in radians:
                x = float(R)*np.cos(theta) + offset
                y = float(R)*np.sin(theta)
                pts.append(pya.DPoint(x, y))
            
            self.cell.shapes(self.l_layer).insert(pya.DPolygon(pts))

class EtchTest_Circ3(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Meander
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Circ3, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("RL", self.TypeList , "Radius list", default=(np.linspace(1000, 1, 101, dtype=int)).tolist())
        self.param("S", self.TypeDouble,
                   "Spacing List", default=50)
        self.param("res", self.TypeInt,
                   "Resolution", default=100.)
        self.param("Rscaling", self.TypeDouble,
                   "Actual width is equal to what is specified, times this scaling parameter", default=1/10.)
        self.param("labelscaling", self.TypeDouble,
                   "Changes units of labels", default=1000)
                   
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Circ2(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        radians = np.linspace(0, 2*np.pi, self.res, endpoint = False)
        
        offset = 0
        for i, R in enumerate(self.RL):
            print(R)
            pts = []
            for theta in radians:
                x = self.Rscaling*float(R)*np.cos(theta) + offset
                y = self.Rscaling*float(R)*np.sin(theta)
                pts.append(pya.DPoint(x, y))
            offset += self.S
            self.cell.shapes(self.l_layer).insert(pya.DPolygon(pts))
            
class ExperimentalOhmics (pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Meander
    """

    def __init__(self):

        # Important: initialize the super class
        super(ExperimentalOhmics, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("X", self.TypeDouble, "X", default=200.)
        self.param("Y", self.TypeDouble, "Y", default=200.)
        self.param("A", self.TypeInt, "Amplitude", default=1)
        self.param("H", self.TypeInt, "Harmonic", default=1)
        self.param("R", self.TypeInt, "Resolution", default=2)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "ExperimentalOhmics(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        pts = []

        edges_x = np.linspace(-1, 1, num=self.R, endpoint=True)
        edges_y = self.A*np.sin(self.H*2*np.pi*edges_x)

        print(edges_x)
        print(edges_y)

        edges_x1 = edges_x*self.X/2
        edges_y1 = -1*edges_y - self.Y/2
        print(edges_x1)
        print(edges_y1)

        for p in zip(edges_x1, edges_y1):
            pts.append(pya.DPoint(p[0], p[1]))

        edges_x2 = edges_y + self.X/2
        edges_y2 = edges_x*self.Y/2
        print(edges_x2)
        print(edges_y2)

        for p in zip(edges_x2, edges_y2):
            pts.append(pya.DPoint(p[0], p[1]))

        edges_x3 = -1*edges_x*self.X/2
        edges_y3 = edges_y + self.Y/2
        print(edges_x3)
        print(edges_y3)

        for p in zip(edges_x3, edges_y3):
            pts.append(pya.DPoint(p[0], p[1]))

        edges_x4 = -1*edges_y - self.X/2
        edges_y4 = -1*edges_x*self.Y/2
        print(edges_x4)
        print(edges_y4)

        for p in zip(edges_x4, edges_y4):
            pts.append(pya.DPoint(p[0], p[1]))

        self.cell.shapes(self.l_layer).insert(pya.DPolygon(pts))

class RCLine(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Serpentine
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
        self.param("text_distance", self.TypeDouble, "Offset parameter between the bottom edge of the RC line, and the label", default=60.0)
        self.param("text_scale", self.TypeDouble, "Scaling parameter for the text size", default=0.02)
    
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
        
        label = pya.TextGenerator.default_generator().text("{}".format(squares), self.text_scale*self.layout.dbu).move(1000*pts[0].x, 1000*pts[0].y - 1000*self.text_distance)
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


class Align(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Serpentine
    """

    def __init__(self):

        # Important: initialize the super class
        super(Align, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        
        self.param("width", self.TypeDouble, "Rectangle width", default=300.0)
        self.param("length", self.TypeDouble, "Rectangle length", default=300.0)
        
        self.param("cwidth", self.TypeDouble, "Cross width", default=200.0)
        self.param("clength", self.TypeDouble, "Cross length", default=200.0)
        self.param("cthick", self.TypeDouble, "Cross thickness", default=10.0)
      
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "Align(L=%s)" % (str(self.l))

    def produce_impl(self):
        lower_left = pya.DPoint(-self.width/2, -self.length/2)
        upper_right = pya.DPoint(self.width/2, self.length/2)
        square = pya.DBox(lower_left, upper_right)
        
        l0 = pya.Region()
        l0.insert(square)
        
        c1 = pya.DPoint(-self.cwidth/2, 0)
        c2 = pya.DPoint(self.cwidth/2, 0)
        p1 = pya.DPath([c1, c2], self.cthick)
        
        l1 = pya.Region()
        l1.insert(p1)
        
        c3 = pya.DPoint(0, -self.clength/2)
        c4 = pya.DPoint(0, self.clength/2)
        p2 = pya.DPath([c3, c4], self.cthick)
        
        l2 = pya.Region()
        l2.insert(p2)
        
        result =l0 - l1 - l2
        self.cell.shapes(self.l_layer).insert(result)

class AlignArray(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Serpentine
    """

    def __init__(self):

        # Important: initialize the super class
        super(AlignArray, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        
        self.param("width", self.TypeDouble, "Rectangle width", default=300.0)
        self.param("length", self.TypeDouble, "Rectangle length", default=300.0)
        
        self.param("cwidth", self.TypeDouble, "Cross width", default=200.0)
        self.param("clength", self.TypeDouble, "Cross length", default=200.0)
        self.param("cthick", self.TypeDouble, "Cross thickness", default=10.0)
        
        self.param("rows", self.TypeInt, "Number of rows", default=2)
        self.param("columns", self.TypeInt, "Number of columns", default=2)
        
        self.param("row_step", self.TypeDouble, "Row step", default=300.0)
        self.param("col_step", self.TypeDouble, "Col step", default=300.0)
        
        self.param("text_distance", self.TypeDouble, "Text distance", default=75.0)
        self.param("text_scale", self.TypeDouble, "Text scaling factor", default=0.04)
    
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "AlignArray(L=%s)" % (str(self.l))

    def produce_impl(self):
        
        scaling_factor = int(1/self.layout.dbu)
        print(scaling_factor)
        x = np.linspace(0, self.rows, endpoint=False, num=self.rows, dtype=int)*self.row_step
        y = np.linspace(0, self.columns, endpoint=False, num=self.columns,)*self.col_step
        
        XX,YY = np.meshgrid(x,y, indexing='ij')
        
        print(XX)
        print(YY)
        
        grid=np.zeros((self.rows,self.columns),dtype='i,i')
        
        for i in range(0, self.rows):
          for j in range(0, self.columns):
            grid[i,j] = (XX[i,j], YY[i,j])
            print(grid[i,j])
        
        for p in grid.flatten():
          c_x = float(p[0])
          c_y = float(p[1])
        
          lower_left = pya.DPoint(c_x-self.width/2, c_y-self.length/2)
          upper_right = pya.DPoint(c_x+self.width/2, c_y+self.length/2)
          square = pya.DBox(lower_left*scaling_factor, upper_right*scaling_factor)
        
          l0 = pya.Region()
          l0.insert(square)

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
          
          label = pya.TextGenerator.default_generator().text("{},{}".format(int(p[0]-x.max()/2), int(p[1]-y.max()/2)), self.text_scale*self.layout.dbu).move(1000*(c_x-self.width/2 + self.width/40), 1000*c_y - 1000*self.text_distance)
          
          result = l0 - l1 - l2 - label
          
          self.cell.shapes(self.l_layer).insert(result)         
          #self.cell.shapes(self.l_layer).insert(label)
        
class RayLib(pya.Library):
    """
    The library where we will put the PCell into 
    """

    def __init__(self):

        # Set the description
        self.description = "Ray's PCell Library"
    
        # Create the PCell declarations
        self.layout().register_pcell("Serpentine", Serpentine())
        self.layout().register_pcell("Meander", Meander())
        self.layout().register_pcell("EtchTest_Box", EtchTest_Box())
        self.layout().register_pcell("EtchTest_Box2", EtchTest_Box2())
        self.layout().register_pcell("EtchTest_Box3", EtchTest_Box3())
        self.layout().register_pcell("EtchTest_Circ", EtchTest_Circ())
        self.layout().register_pcell("EtchTest_Circ2", EtchTest_Circ2())
        self.layout().register_pcell("EtchTest_Circ3", EtchTest_Circ3())
        
        self.layout().register_pcell("ExperimentalOhmics", ExperimentalOhmics())
        self.layout().register_pcell("RCLine", RCLine())
        self.layout().register_pcell("Align", Align())
        self.layout().register_pcell("AlignArray", AlignArray())
        
        # Register us with the name "SerpentineLib".
        self.register("RayLib")


# Instantiate and register the library
RayLib()
