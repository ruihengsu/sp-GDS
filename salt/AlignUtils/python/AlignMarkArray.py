import pya
import math
import numpy as np

class AlignMarkArray(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Serpentine
    """

    def __init__(self):

        # Important: initialize the super class
        super(AlignMarkArray, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))

        self.param("width", self.TypeDouble, "Rectangle width", default=300.0)
        self.param("length", self.TypeDouble,
                   "Rectangle length", default=300.0)

        self.param("cwidth", self.TypeDouble, "Cross width", default=200.0)
        self.param("clength", self.TypeDouble, "Cross length", default=200.0)
        self.param("cthick", self.TypeDouble, "Cross thickness", default=10.0)

        self.param("rows", self.TypeInt, "Number of rows", default=2)
        self.param("columns", self.TypeInt, "Number of columns", default=2)

        self.param("row_step", self.TypeDouble, "Row step", default=300.0)
        self.param("col_step", self.TypeDouble, "Col step", default=300.0)

        self.param("text_distance", self.TypeDouble,
                   "Text distance", default=75.0)
        self.param("text_scale", self.TypeDouble,
                   "Text scaling factor", default=0.04)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "AlignMarkArray(L=%s)" % (str(self.l))

    def produce_impl(self):

        scaling_factor = int(1/self.layout.dbu)
        print(scaling_factor)
        x = np.linspace(0, self.rows, endpoint=False,
                        num=self.rows, dtype=int)*self.row_step
        y = np.linspace(0, self.columns, endpoint=False,
                        num=self.columns,)*self.col_step

        XX, YY = np.meshgrid(x, y, indexing='ij')

        print(XX)
        print(YY)

        grid = np.zeros((self.rows, self.columns), dtype='i,i')

        for i in range(0, self.rows):
            for j in range(0, self.columns):
                grid[i, j] = (XX[i, j], YY[i, j])
                print(grid[i, j])

        for p in grid.flatten():
            c_x = float(p[0])
            c_y = float(p[1])

            lower_left = pya.DPoint(c_x-self.width/2, c_y-self.length/2)
            upper_right = pya.DPoint(c_x+self.width/2, c_y+self.length/2)
            square = pya.DBox(lower_left*scaling_factor,
                              upper_right*scaling_factor)

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

            label = pya.TextGenerator.default_generator().text("{},{}".format(int(p[0]-x.max()/2), int(p[1]-y.max(
            )/2)), self.text_scale*self.layout.dbu).move(1000*(c_x-self.width/2 + self.width/40), 1000*c_y - 1000*self.text_distance)

            result = l0 - l1 - l2 - label

            self.cell.shapes(self.l_layer).insert(result)
            # self.cell.shapes(self.l_layer).insert(label)
