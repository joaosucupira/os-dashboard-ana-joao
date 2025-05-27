from Models.GerenciadorMemoria import GerenciadorMemoria
from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria
from Views.TabelaMemoriaView import TabelaMemoriaView

class MemoriaController:
    def __init__(self, master):
        self.model = GerenciadorMemoria()
        self.view = TabelaMemoriaView(master=master)
        self.atualizar_tabela_memoria()

    def atualizar_tabela_memoria(self):
        dados_memoria = self.model.atualizaDados()
        self.view.mostrar_memoria(dados_memoria)

    def mostrar(self):
        self.view.deiconify()
        self.atualizar_tabela_memoria()