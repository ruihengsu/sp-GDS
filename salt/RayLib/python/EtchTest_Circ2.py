import pya
import numpy as np

class EtchTest_Circ2(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the EtchTest_Circ2
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Circ2, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("RL", self.TypeList, "Radius list",
                   default=[50, 40, 30, 20, 10])
        self.param("SL", self.TypeList,
                   "Spacing List", default=[100, 100, 100, 30, 30])
        self.param("res", self.TypeInt,
                   "Resolution", default=100.)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "EtchTest_Circ2(Layer=%s)" % (str(self.l))

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        assert len(self.RL) == len(self.SL)
        radians = np.linspace(0, 2*np.pi, self.res, endpoint=False)

        offset = 0
        for i, R in enumerate(self.RL):
            offset += float(self.SL[i])
            print(R)
            pts = []
            for theta in radians:
                x = float(R)*np.cos(theta) + offset
                y = float(R)*np.sin(theta)
                pts.append(pya.DPoint(x, y))

            self.cell.shapes(self.l_layer).insert(pya.DPolygon(pts))