import pya
import numpy as np


class CircularSerpentine(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the CircularSerpentine
    """

    def __init__(self):

        # Important: initialize the super class
        super(CircularSerpentine, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("l_inner", self.TypeDouble,
                   "length of inner arm", default=10)
        self.param("l_outer", self.TypeDouble,
                   "length of outer arm", default=10)
        self.param("pitch", self.TypeDouble,
                   "Radial pitch between rings", default=10)
        self.param("theta", self.TypeDouble, "Angle to cover", default=45)
        self.param("thick", self.TypeInt,
                   "Thickness of serpentine line", default=2)
        self.param("n", self.TypeInt, "Number of rings", default=10)
        self.param("res", self.TypeInt,
                   "Resolution of the smallest ring of the serpentine", default=3)
        self.param("rot", self.TypeDouble, "Rotation", default=0)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "CircularSerpentine(L=%s)" % (str(self.l))

    def produce_impl(self):

        pts = list()
        pts += [pya.DPoint(0, 0), pya.DPoint(0, self.l_inner)]

        # convert to radians
        theta = (self.theta)*np.pi/180

        dtheta = theta/(2*self.res)
        for p in range(1, self.res+1):
            x = self.l_inner*np.cos(p*dtheta + np.pi/2)
            y = self.l_inner*np.sin(p*dtheta + np.pi/2)
            pts.append(pya.DPoint(x, y))

        for i in range(1, self.n+1):
            dtheta = ((-1)**i)*theta/((i+2)*self.res)
            print(dtheta)
            if i % 2 == 0:
                shift = np.pi/2 - theta/2
            else:
                shift = theta/2 + np.pi/2

            for p in range(0, (i+2)*self.res+1):
                ring_r = (self.l_inner + i*self.pitch)
                x = ring_r*np.cos(p*dtheta + shift)
                y = ring_r*np.sin(p*dtheta + shift)
                pts.append(pya.DPoint(x, y))

        if self.n % 2 == 0:
            dtheta = -1*theta/(2*self.res*(self.n))
            shift = theta/2 + np.pi/2
        else:
            dtheta = theta/(2*self.res*(self.n))
            shift = np.pi/2 - theta/2
        for p in range(0, (self.res)*(self.n)+1):
            ring_r = (self.l_inner + (self.n+1)*self.pitch)
            x = ring_r*np.cos(p*dtheta + shift)
            y = ring_r*np.sin(p*dtheta + shift)
            pts.append(pya.DPoint(x, y))

        pts.append(pya.DPoint(0, self.l_outer +
                   self.l_inner + self.pitch*(self.n + 1)))

        tt = pya.DCplxTrans(1,  self.rot, False, 0, 0)

        self.cell.shapes(self.l_layer).insert(tt*pya.DPath(pts, self.thick))

# class Serpentine(pya.PCellDeclarationHelper):
#     """
#     The PCell declaration for Serpentine
#     """

#     def __init__(self):

#         # Important: initialize the super class
#         super(Serpentine, self).__init__()

#         # declare the parameters
#         self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
#         self.param("n", self.TypeInt,
#                    "Number of points per full turn", default=5)
#         self.param("w", self.TypeDouble, "The width", default=1.0)
#         self.param("u", self.TypeDouble, "One turn's pitch", default=2.0)
#         self.param("s", self.TypeDouble, "The turn's length", default=20.0)

#     def display_text_impl(self):
#         # Provide a descriptive text for the cell
#         return "Serpentine(L=%s,S=%.12g,U=%.12g)" % (str(self.l), self.s, self.u)

#     def produce_impl(self):

#         # This is the main part of the implementation: create the layout

#         # compute the Serpentine: generate a list of spine points for the path and then
#         # create the path

#         pts = []

#         x = 0.0
#         y = 0.0

#         for i in range(0, self.n):
#             pts.append(pya.DPoint(x, y))
#             x += self.u
#             pts.append(pya.DPoint(x, y))
#             if (i % 2) == 0:
#                 y += self.s
#             else:
#                 y -= self.s
#             pts.append(pya.DPoint(x, y))

#         # One last point to move to the end location
#         x += self.u
#         pts.append(pya.DPoint(x, y))

#         # create the shape
#         self.cell.shapes(self.l_layer).insert(pya.DPath(pts, self.w))


class RayDev(pya.Library):
    """
    The library where we will put the PCell into 
    """

    def __init__(self):

        # Set the description
        self.description = "Ray De's PCell Library"

        # Create the PCell declarations

        # self.layout().register_pcell("OverlayAlignMarkArray", OverlayAlignMarkArray())

        self.layout().register_pcell("CircularSerpentine", CircularSerpentine())
        # Register us with the name "SerpentineLib".
        self.register("RayDev")


# Instantiate and register the library
RayDev()
