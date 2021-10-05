class OverlayAlignMarkArray(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the OverlayAlignMarkArray
    """

    def __init__(self):

        # Important: initialize the super class
        super(OverlayAlignMarkArray, self).__init__()

        # declare the parameters
        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
    
        self.param("width", self.TypeDouble, "Rectangle width", default=300.0)
        self.param("length", self.TypeDouble, "Rectangle length", default=300.0)

        self.param("cwidth", self.TypeDouble, "Cross width", default=200.0)
        self.param("clength", self.TypeDouble, "Cross length", default=200.0)
        self.param("cthick", self.TypeDouble, "Cross thickness", default=10.0)

        self.param("othick", self.TypeDouble, "Overlay thickness", default=5.0)
        self.param("olength", self.TypeDouble, "Overlay length", default=80.0)
        self.param("opitch", self.TypeDouble, "Overlay pitch", default=15.0)
        self.param("oN", self.TypeInt, "Number of overlay marks", default=4)
                
        self.param("oxp", self.TypeBoolean, "Enable +x overlay marks", default=True)
        self.param("oxn", self.TypeBoolean, "Enable -x overlay marks", default=True)
        self.param("oyp", self.TypeBoolean, "Enable +y overlay marks", default=True)
        self.param("oyn", self.TypeBoolean, "Enable -y overlay marks", default=True)
        
        self.param("rows", self.TypeInt, "Number of rows", default=2)
        self.param("columns", self.TypeInt, "Number of columns", default=2)

        self.param("row_step", self.TypeDouble, "Row step", default=300.0)
        self.param("col_step", self.TypeDouble, "Col step", default=300.0)

        self.param("text_distance", self.TypeDouble,
                   "Text distance", default=75.0)
        self.param("text_scale", self.TypeDouble,
                   "Text scaling factor", default=0.04)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "OverlayAlignMarkArray(L=%s)" % (str(self.l))

    def produce_impl(self):

        scaling_factor = int(1/self.layout.dbu)
        print(scaling_factor)
        x = np.linspace(0, self.rows, endpoint=False,
                        num=self.rows, dtype=int)*self.row_step
        y = np.linspace(0, self.columns, endpoint=False,
                        num=self.columns,)*self.col_step

        XX, YY = np.meshgrid(x, y, indexing='ij')

        grid = np.zeros((self.rows, self.columns), dtype='i,i')

        for i in range(0, self.rows):
            for j in range(0, self.columns):
                grid[i, j] = (XX[i, j], YY[i, j])
                print(grid[i, j])

        for p in grid.flatten():
            c_x = float(p[0])
            c_y = float(p[1])

            lower_left = pya.DPoint(c_x-self.width/2, c_y-self.length/2)*scaling_factor
            upper_right = pya.DPoint(c_x+self.width/2, c_y+self.length/2)*scaling_factor
            square = pya.DBox(lower_left,
                                       upper_right)

            l0 = pya.Region()
            l0.insert(square)

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

            label = pya.TextGenerator.default_generator().text("{},{}".format(int(p[0]-x.max()/2), 
                                                                              int(p[1]-y.max()/2)), 
                                                               self.text_scale*self.layout.dbu).move(1000*(c_x-self.width/2 + self.width/40), 
                                                                                                     1000*c_y - 1000*self.text_distance)

            result = l0 - l1 - l2 - label
            
            for i in range(self.oN):

                if self.oxn:
                    c5 = pya.DPoint(c1.x + i*self.opitch*scaling_factor,  
                                            c1.y + scaling_factor*self.olength/2)   
                    c6 = pya.DPoint(c1.x + i*self.opitch*scaling_factor, 
                                            c1.y - scaling_factor*self.olength/2)
                    p3 = pya.DPath([c5, c6], self.othick*scaling_factor)
                    l3 = pya.Region()
                    l3.insert(p3)
                    result -= l3
                    
                if self.oxp:
                    c7 = pya.DPoint(c2.x - i*self.opitch*scaling_factor,  
                                            c2.y + scaling_factor*self.olength/2)   
                    c8 = pya.DPoint(c2.x - i*self.opitch*scaling_factor,  
                                            c2.y - scaling_factor*self.olength/2)
                    p4 = pya.DPath([c7, c8], self.othick*scaling_factor)
                    l4 = pya.Region()
                    l4.insert(p4)
                    result -= l4
                
                if self.oyn:
                    c9 = pya.DPoint(c3.x + scaling_factor*self.olength/2,  
                                            c3.y + i *self.opitch*scaling_factor)   
                    c10 = pya.DPoint(c3.x - scaling_factor*self.olength/2,  
                                            c3.y + i *self.opitch*scaling_factor)   
                    p5 = pya.DPath([c9, c10], self.othick*scaling_factor)
                    l5 = pya.Region()
                    l5.insert(p5)
                    result -= l5
                
                if self.oyp:
                    c11 = pya.DPoint(c4.x + scaling_factor*self.olength/2, 
                                            c4.y - i *self.opitch*scaling_factor)   
                    c12 = pya.DPoint(c4.x - scaling_factor*self.olength/2, 
                                            c4.y - i *self.opitch*scaling_factor)
                    p6 = pya.DPath([c11, c12], self.othick*scaling_factor)
                    l6 = pya.Region()
                    l6.insert(p6)
                    result -= l6
                    
            self.cell.shapes(self.l_layer).insert(result)