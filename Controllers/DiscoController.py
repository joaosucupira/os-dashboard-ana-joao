import os
from Models.GerenciadorDisco import GerenciadorDisco
from Views.DiscoView import DiscoView

class DiscoController:
    def __init__(self, master):
        self.model = GerenciadorDisco()
        self.view = DiscoView(master=master, nav_callback=self.navegar_para)
        self.current_path = "/"

        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_interface()

    def atualizar_interface(self):
        particoes = self.model.get_partitions_info()
        self.view.mostrar_particoes(particoes)
        
        self.atualizar_navegador()

    def atualizar_navegador(self):
        conteudo = self.model.list_directory_contents(self.current_path)
        self.view.mostrar_arquivos(self.current_path, conteudo)

    def navegar_para(self, novo_path):
        if novo_path == "..":
            self.current_path = os.path.dirname(self.current_path)
            if not self.current_path or self.current_path == "/":
                self.current_path = "/"
        else:
            self.current_path = novo_path
        
        self.atualizar_navegador()

    def fechar(self):
        self.view.destroy()