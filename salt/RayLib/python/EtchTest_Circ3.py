import pya
import numpy as np

class EtchTest_Circ3(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the EtchTest_Circ3
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Circ3, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("RL", self.TypeList, "Radius list", default=(
            np.linspace(1000, 1, 101, dtype=int)).tolist())
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
        return "EtchTest_Circ3(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        radians = np.linspace(0, 2*np.pi, self.res, endpoint=False)

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