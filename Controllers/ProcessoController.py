from Models.GerenciadorProcessos import GerenciadorProcessos
from Views.TabelaProcessosView import TabelaProcessosView

class ProcessoController:
    def __init__(self):
        self.model = GerenciadorProcessos()
        self.view = TabelaProcessosView()
        self.atualizar_tabela_periodicamente()
        self.view.mainloop()

    def atualizar_tabela_periodicamente(self):
        processos = self.model.listar_processos_e_usuarios()
        self.view.mostrar_processos(processos)
        # Atualiza a cada 2 segundos (2000 ms)
        self.view.after(2000, self.atualizar_tabela_periodicamente)