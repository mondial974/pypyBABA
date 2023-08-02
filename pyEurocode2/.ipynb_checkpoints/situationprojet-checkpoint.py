class SituationProjet:
    
    def __init__(self, situation='Durable'):
        self.situation = situation
           

    def gc(self):
        if self.situation == 'Durable':
            return 1.5
              
        if self.situation == 'Accidentelle':
            return  1.2 
          
    
    def gs(self):
        if self.situation == 'Durable':
            return 1.15
        
        if self.situation == 'Accidentelle':
            return 1.
        
     
    def __repr__(self):
        print(f"Situation de projet : {self.situation}")
        print(f"gc = {self.gc()}")
        print(f"gs = {self.gs()}")
                        
        return ""