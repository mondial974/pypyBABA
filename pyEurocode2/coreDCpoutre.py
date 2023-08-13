class DCPoutreRectangulaire:
    def __init__(self, beton, acier, bw, h, c):
        self.beton = beton
        self.acier = acier
        self.bw = bw
        self.h = h
        self.c = c

    def Ac(self):
        return self.bw * self.h

    def d(self):
        return self.h - self.c

    def Asmin(self):
        fctm = self.beton.fctm()
        fyk = self.acier.fyk()
        bw = self.bw
        d = self.d()
        Asmin1 = 0.26 * fctm / fyk * bw * d
        Asmin2 = 0.0013 * bw * d
        Asmin = max(Asmin1, Asmin2)
        return Asmin

    def Asmax(self):
        return 0.04 * self.Ac()
