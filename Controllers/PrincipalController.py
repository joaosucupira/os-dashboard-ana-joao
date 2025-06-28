from Views.ViewPrincipal import ViewPrincipal
from Views.TabelaProcessosView import TabelaProcessosView
from Views.TabelaProcessosArquivosView import TabelaProcessosArquivosView
from Controllers.MemoriaController import MemoriaController
from Controllers.ProcessoController import ProcessoController
from Controllers.ArquivosController import ArquivosController

class PrincipalController:
    def __init__(self):
        self.view_p = ViewPrincipal(self.executar_tabela_processos, self.executar_tabela_memoria, self.executar_tabela_arquivos, self.executar_arvore_disco)

    # chama o controler dos processos e cpu
    def executar_tabela_processos(self):
        ProcessoController(self.view_p)

    # chama o controler da memoria
    def executar_tabela_memoria(self):
        MemoriaController(self.view_p)

    # chama o controler da memoria
    def executar_tabela_arquivos(self):
        ArquivosController(self.view_p)     
        
    def executar_arvore_disco(self):
        raise NotImplementedError("Funcionalidade de acesso a diretórios do disco ainda não implementada.")

    def executar(self):
        self.view_p.mainloop()

    def fechar(self):
        if self.view_p:
            # Fecha view filha de processos, se existir e estiver aberta
            if hasattr(self, 'processos_controller') and self.processos_controller:
                if hasattr(self.processos_controller, 'view_p') and self.processos_controller.view_p.winfo_exists():
                    self.processos_controller.view_p.destroy()
            # Fecha view filha de memória, se existir e estiver aberta
            if hasattr(self, 'memoria_controller') and self.memoria_controller:
                if hasattr(self.memoria_controller, 'view_p') and self.memoria_controller.view_p.winfo_exists():
                    self.memoria_controller.view_p.destroy()
            self.view_p.fechar()