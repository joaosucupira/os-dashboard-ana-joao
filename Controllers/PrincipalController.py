from Views.ViewPrincipal import ViewPrincipal
from Views.TabelaProcessosView import TabelaProcessosView
from Controllers.ProcessoController import ProcessoController

class PrincipalController:
    def __init__(self):
        self.view_p = ViewPrincipal(self.executar_tabela_processos)


    def executar_tabela_processos(self):
        ProcessoController(self.view_p)

    

    def executar(self):
        self.view_p.mainloop()

