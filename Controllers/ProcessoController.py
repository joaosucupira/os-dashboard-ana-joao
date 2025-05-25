from Models.GerenciadorProcessos import GerenciadorProcessos
from Views.TabelaProcessosView import TabelaProcessosView

import time
import threading

class ProcessoController:
    def __init__(self, view):
        self.processos = []
        self.view = view

        self.executar_tabela()

    def atualizar_tabela_periodicamente(self):
        self.processos = self.model.listar_processos_e_usuarios()
        self.view.mostrar_processos(self.processos)

        # TKINTER AFTER: Atualiza a cada 2 segundos
        self.view.after(2000, self.atualizar_tabela_periodicamente)

    def executar_tabela(self):
        self.model = GerenciadorProcessos()
        self.view = TabelaProcessosView()
        self.atualizar_tabela_periodicamente()
        self.view.mainloop()
