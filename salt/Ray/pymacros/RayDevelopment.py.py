import pya 

import pya
import numpy as np
import pya
import numpy as np




class RayDev(pya.Library):
    """
    The library where we will put the PCell into 
    """

    def __init__(self):

        # Set the description
        self.description = "Ray De's PCell Library"

        # Create the PCell declarations
        
        # self.layout().register_pcell("OverlayAlignMarkArray", OverlayAlignMarkArray())
        
        
        # Register us with the name "SerpentineLib".
        self.register("RayDev")

# Instantiate and register the library
RayDev()