class BlocMaconnerie:
    
    def __init__(self, groupe, t, fvk, fb, fd, gammaM):
        self.groupe = groupe
        self.t = t
        self.fvk = fvk
        self.fb = fb
        self.fd = fd
        self.gammaM = gammaM
        
    def fvd(self):
        fvk = self.fvk
        gammaM = self.gammaM
        return  fvk / gammaM
    
    def emu(self):
        groupe = self.groupe
        dict_emu = {1 : 0.0035, 2: 0.002, 3: 0.002, 4: 0.002}
        return dict_emu[groupe]    
        