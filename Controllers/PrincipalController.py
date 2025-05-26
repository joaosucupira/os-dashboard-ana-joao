from Views.ViewPrincipal import ViewPrincipal
from Views.TabelaProcessosView import TabelaProcessosView
from Controllers.MemoriaController import MemoriaController
from Controllers.ProcessoController import ProcessoController

class PrincipalController:
    def __init__(self):
        self.view_p = ViewPrincipal(self.executar_tabela_processos, self.executar_tabela_memoria)


    def executar_tabela_processos(self):
        ProcessoController(self.view_p)

    # chama o controler da memoria
    def executar_tabela_memoria(self):
        MemoriaController(self.view_p)    

    def executar(self):
        self.view_p.mainloop()
