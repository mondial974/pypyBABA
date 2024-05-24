class SituationProjet:
    
    def __init__(self, situation='Durable'):
        self.situation = situation
           

    def gamma_c(self):
        if self.situation == 'Durable':
            return 1.5
              
        if self.situation == 'Accidentelle':
            return  1.2 
          
    
    def gamma_s(self):
        if self.situation == 'Durable':
            return 1.15
        
        if self.situation == 'Accidentelle':
            return 1.
        
     
    def __repr__(self):
        print(f"Situation de projet : {self.situation}")
        print(f"gamma_c = {self.gamma_c()}")
        print(f"gamma_s = {self.gamma_s()}")
                        
        return ""