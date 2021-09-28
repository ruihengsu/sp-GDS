import pya
import numpy as np

class EtchTest_Box3(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the EtchTest_Box3
    """

    def __init__(self):

        # Important: initialize the super class
        super(EtchTest_Box3, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("L", self.TypeDouble, "Length", default=1000)
        self.param("WL", self.TypeList, "Width List", default=(
            np.linspace(1000, 1, 101, dtype=int)).tolist())
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
        pcell_decl = lib.layout().pcell_declaration("TEXT")
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
            label = pya.TextGenerator.default_generator().text("{}".format(int(float(
                self.WL[i])*self.labelscaling)), 0.05*self.layout.dbu).move(1000*pts[0].x, 1000*pts[0].y - 1000*self.text_distance)

            self.cell.shapes(self.l_layer).insert(label)

            x += float(self.spacing)
            y -= float(self.L)