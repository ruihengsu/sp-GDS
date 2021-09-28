import pya
import numpy as np

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
        self.param("ml", self.TypeDouble,
                   "Length of meander line", default=1000.0)
        self.param("t", self.TypeDouble,
                   "Additional Thickness", default=1000.0)
        self.param("bl", self.TypeDouble, "Bond line length", default=1000.0)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "Meander(Layer=%s,Length=%.12g,Pitch=%.12g,Width=%.12g)" % (str(self.l), self.ml, self.u, self.w)

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        # compute the Serpentine: generate a list of spine points for the path and then
        # create the path
        print("NEW")
        pts = []

        box_pts = dict()

        x = 0.0
        y = self.ml/2.

        pts.append(pya.DPoint(x, y))
        y -= self.ml/2.
        print(x, y)
        pts.append(pya.DPoint(x, y))

        for i in range(0, self.n):

            x += self.u
            print(x, y)
            pts.append(pya.DPoint(x, y))

            if (i % 2) == 0:
                y += self.ml
            else:
                y -= self.ml
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
            y -= self.ml/2
        else:
            y = self.ml/2
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
