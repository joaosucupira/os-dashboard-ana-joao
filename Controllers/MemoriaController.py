from Models.GerenciadorMemoria import GerenciadorMemoria
from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria
from Views.TabelaMemoriaView import TabelaMemoriaView

class MemoriaController:
    def __init__(self, master):
        self.model = GerenciadorMemoria()
        self.model_processos = GerenciadorProcessosMemoria()
        self.view = TabelaMemoriaView(master=master)
        self.atualizar_tabela_memoria()

    def atualizar_tabela_memoria(self):
        dados_memoria = self.model.atualizaDados()
        dados_processos = self.model_processos.listar_processos_e_usuarios()
        self.view.mostrar_memoria(dados_memoria, dados_processos)

    # def mostrar(self):
    #     self.view.deiconify()
    #     self.atualizar_tabela_memoria()