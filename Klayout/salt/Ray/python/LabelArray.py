import pya
import numpy as np


class LabelArray(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the LabelArray
    """

    def __init__(self):
        # Important: initialize the super class
        super(LabelArray, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("horizontal", self.TypeBoolean,
                   "Horizontal labels?", default=True)
        self.param("labels", self.TypeList,
                   "List of labels", default=[1, 2, 3])
        self.param("text_pitch", self.TypeDouble,
                   "Distance between adjacent Labels", default=10.)
        self.param("text_scale", self.TypeDouble,
                   "Text scaling factor", default=10)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "LabelArray(Layer=%s)" % (str(self.l))

    def produce_impl(self):

        scaling_factor = int(1/self.layout.dbu)

        for i, lab in enumerate(self.labels):
            label = pya.TextGenerator.default_generator().text(
                "{}".format(lab), self.layout.dbu/self.text_scale)

            if self.horizontal:
                label = label.move(i*scaling_factor*self.text_pitch, 0)
            else:
                label = label.move(0, -i*scaling_factor*self.text_pitch)

            self.cell.shapes(self.l_layer).insert(label)
