import pya
import numpy as np


class LabelArray_VariablePitch(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the LabelArray_VariablePitch
    """

    def __init__(self):
        # Important: initialize the super class
        super(LabelArray_VariablePitch, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("horizontal", self.TypeBoolean,
                   "Horizontal labels?", default=True)
        self.param("labels", self.TypeList,
                   "List of labels", default=["1", "2", "3"])           
        self.param("text_pitch", self.TypeList,
                   "Distance between adjacent Labels", default = np.array([0, 50, 100], dtype=int).tolist())
        self.param("text_scale", self.TypeDouble,
                   "Text scaling factor", default=10)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "LabelArray_VariablePitch(Layer=%s)" % (str(self.l))

    def produce_impl(self):
      
        print(self.text_pitch)

        scaling_factor = int(1/self.layout.dbu)
        for i, lab in enumerate(self.labels):
            lab = lab.strip()
            label = pya.TextGenerator.default_generator().text(
                "{}".format(lab), self.layout.dbu/self.text_scale)

            if self.horizontal:
                label = label.move(i*scaling_factor*float(self.text_pitch[i]), 0)
            else:
                label = label.move(0, -i*scaling_factor*float(self.text_pitch[i]))

            self.cell.shapes(self.l_layer).insert(label)

