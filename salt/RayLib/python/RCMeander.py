import pya
import numpy as np


class RCMeander(pya.PCellDeclarationHelper):
    """
    The PCell declaration of a meander line to be used in a RC distributed filter
    """

    def __init__(self):

        super(RCMeander, self).__init__()
        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("n", self.TypeInt, "Number of turns", default=9)
        self.param("w", self.TypeDouble, "Width of meander line", default=30.)
        self.param("p", self.TypeDouble, "Pitch", default=180.0)
        self.param("ml", self.TypeDouble,
                   "Length of meander line", default=1000.0)
        self.param("t", self.TypeDouble,
                   "Additional Thickness", default=1000.0)
        self.param("bl", self.TypeDouble, "Bond line length", default=1000.0)
        self.param("bw", self.TypeDouble, "Bond pad width", default=300.0)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "RCMeander(Layer=%s,Length=%.12g,Pitch=%.12g,Width=%.12g)" % (str(self.l), self.ml, self.p, self.w)

    def produce_impl(self):
        pts = []
        box_pts = dict()

        x = 0.0
        y = self.ml/2.

        pts.append(pya.DPoint(x, y))
        y -= self.ml/2.
        pts.append(pya.DPoint(x, y))

        for i in range(0, self.n):

            x += self.p
            pts.append(pya.DPoint(x, y))

            if (i % 2) == 0:
                y += self.ml
            else:
                y -= self.ml

            pts.append(pya.DPoint(x, y))

            if (i % 2) == 0:
                box_pts[i] = (pya.DPoint(pts[-2].x + self.w/2, pts[-2].y - self.w/2),
                              pya.DPoint(pts[-3].x - self.w/2, pts[-2].y - self.t - self.w/2))

            else:
                box_pts[i] = (pya.DPoint(pts[-2].x + self.w/2, pts[-2].y + self.w/2),
                              pya.DPoint(pts[-3].x - self.w/2, pts[-2].y + self.t + self.w/2))

        # One last point to move to the end location
        x += self.p
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
        pts.append(pya.DPoint(x, y))

        for p in pts:
            print(p.x, p.y)

        path = pya.DPath(pts, self.w)
        path_area = path.area()
       # m = obj.trans.mag * layout.dbu
        #total_area += a * m * m
        # create the shape
        self.cell.shapes(self.l_layer).insert(path)

        for k in box_pts.keys():
            self.cell.shapes(self.l_layer).insert(
                pya.DBox(box_pts[k][0], box_pts[k][1]))

        bond_line_right_pts = []
        bond_line_right_pts.append(pya.DPoint(pts[0].x + self.w/2, pts[0].y))
        bond_line_right_pts.append(pya.DPoint(
            pts[0].x - self.bl - self.w/2, pts[0].y))

        bond_path_right = pya.DPath(bond_line_right_pts, self.w)
        self.cell.shapes(self.l_layer).insert(bond_path_right)

        bond_line_left_pts = []
        bond_line_left_pts.append(pya.DPoint(pts[-1].x - self.w/2, pts[-1].y))
        bond_line_left_pts.append(pya.DPoint(
            pts[-1].x + self.bl + self.w/2, pts[-1].y))
        bond_paths_left = pya.DPath(bond_line_left_pts, self.w)

        self.cell.shapes(self.l_layer).insert(bond_paths_left)
        bond_line_area = bond_paths_left.area() - self.w**2
        print("Total area: {} um".format(path_area + bond_line_area))

        bond_pad_pts_right = []
        bond_pad_pts_right.append(pya.DPoint(
            bond_line_right_pts[-1].x - self.bw, bond_line_right_pts[-1].y-self.bw/2))
        bond_pad_pts_right.append(pya.DPoint(
            bond_line_right_pts[-1].x, bond_line_right_pts[-1].y+self.bw/2))
        self.cell.shapes(self.l_layer).insert(
            pya.DBox(bond_pad_pts_right[0], bond_pad_pts_right[1]))

        bond_pad_pts_left = []
        bond_pad_pts_left.append(pya.DPoint(
            bond_line_left_pts[-1].x + self.bw, bond_line_left_pts[-1].y-self.bw/2))
        bond_pad_pts_left.append(pya.DPoint(
            bond_line_left_pts[-1].x, bond_line_left_pts[-1].y+self.bw/2))
        self.cell.shapes(self.l_layer).insert(
            pya.DBox(bond_pad_pts_left[0], bond_pad_pts_left[1]))

        # the number of squares without accouting for additional rectangular pads is
        length = self.bl + (self.n + 1)*(self.ml - self.w) + \
            (self.n + 1)*(self.p - self.w)
        squares_mod = length/self.w + (2*self.n + 4)/2
        squares = length/self.w + (2*self.n + 4)

        print("Turning points: {}".format(2*self.n + 4))
        # valid iff the pitch and length of meander line are both non-zero
        # this value ignores the contribution from the bonf pads
        print("Squares: {}".format(squares))
        print("Squares: {} (modified)".format(squares_mod))

        # the length of the meander line, without accounting for the bond pads
        meander_length = 2*self.bl + (self.n+1)*self.p + self.w
        print("Length: {} (modified)".format(meander_length))