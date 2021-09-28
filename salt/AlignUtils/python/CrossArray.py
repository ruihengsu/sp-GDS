import pya
import numpy as np

class CrossArray(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the CrossArray
    """

    def __init__(self):

        # Important: initialize the super class
        super(CrossArray, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))

        self.param("cwidth", self.TypeDouble, "Cross width", default=200.0)
        self.param("clength", self.TypeDouble, "Cross length", default=200.0)
        self.param("cthick", self.TypeDouble, "Cross thickness", default=10.0)

        self.param("rows", self.TypeInt, "Number of rows", default=2)
        self.param("columns", self.TypeInt, "Number of columns", default=2)

        self.param("row_step", self.TypeDouble, "Row step", default=300.0)
        self.param("col_step", self.TypeDouble, "Col step", default=300.0)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "CrossArray(L=%s)" % (str(self.l))

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

            result = l1 + l2

            self.cell.shapes(self.l_layer).insert(result)
            # self.cell.shapes(self.l_layer).insert(label)
