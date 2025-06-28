# Model especializado em coletar informações do processo especidigo atraves de seu identificador

from utils.util_diretorio import GerenciadorDiretorio
from Models.GerenciadorArquivos import GerenciadorArquivos

class GerenciadorDetalhesArq:
    def __init__(self, pid):
        self.pid = str(pid)
        self.proc_dir = f'/proc/{self.pid}'
        self.arquivos_info = []
        self.ga = GerenciadorArquivos()
        

    # Carregamento dos arquivos abertos do processo
    def carregar_arquivos(self):

        fd_path = f'{self.proc_dir}/fd'
        with GerenciadorDiretorio(fd_path) as gd:
            for entry in gd:
                if entry.is_symlink():
                    try:
                        target = entry.readlink()
                        if target.startswith("/"):
                            fd_info = {
                                "fd": entry.name,
                                "caminho": target
                            }
                        self.arquivos_info.append(fd_info)
                    except Exception:
                        continue

        # task_dir = f'{self.proc_dir}/task'
        # with GerenciadorDiretorio(task_dir) as gd:
        #     for entry in gd:
        #         tid = entry.name
        #         # ignorando diretorios que nao sao processos
        #         if tid == "." or tid == ".." : continue 

        #         thread_info = {"tid": tid}
        #         status_path = f'{task_dir}/{tid}/status'

        #         try:
        #             with open(status_path, "r") as f:
        #                 for line in f:

        #                     if line.startswith("Name:"):
        #                         thread_info["name"] = line.split()[1]
        #                     if line.startswith("State:"):
        #                         thread_info["state"] = state_id_para_nome(line.split()[1])

        #         except Exception:
        #             thread_info["name"] = "?"
        #             thread_info["state"] = "?"

        #         self.threads_info.append(thread_info)

    def get_info_arquivos(self): 
        return self.arquivos_info

    def carregar_detalhes_processo(self):
        self.carregar_arquivos()
        
    
