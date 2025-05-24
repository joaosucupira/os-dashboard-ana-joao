# Mediador entre model e view 
from model import Model
from view import DashboardUI

# Classe principal
class Controller:
    def __init__(self, model, view):
        self.modelo = model
        self.vista = view
        self.check_view_model()

        
    def check_view_model(self):
        if(self.modelo == None or self.vista == None):
            print("Sem modelo ou vista") 
            exit(1)