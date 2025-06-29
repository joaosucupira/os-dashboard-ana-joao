# Model especializado em coletar informações do processo especidigo atraves de seu identificador

from utils.util_diretorio import GerenciadorDiretorio
from Models.GerenciadorArquivos import GerenciadorArquivos

class GerenciadorDetalhesArq:
    def __init__(self, pid):
        self.pid = str(pid)
        self.proc_dir = f'/proc/{self.pid}'
        self.fd_dir = f'{self.proc_dir}/fd'
        self.infos = []
        self.ga = GerenciadorArquivos()
        

    # Carregamento dos arquivos abertos do processo
    def carregar_infos(self):

        
        with GerenciadorDiretorio(self.fd_dir) as gd:
            for entry in gd:
                if entry.is_symlink():
                    try:
                        target = entry.readlink()
                        if target.startswith("/"):
                            fd_info = {
                                "fd": entry.name,
                                "caminho": target,
                                "tipo": "arquivo"
                            }
                            self.infos.append(fd_info)
                        elif target.startswith("socket:"):
                            fd_info = {
                                "fd": entry.name,
                                "caminho": target,
                                "tipo": "socket"
                            }
                            self.infos.append(fd_info)
                        elif target.startswith("pipe:"):
                            fd_info = {
                                "fd": entry.name,
                                "caminho": target,
                                "tipo": "pipe"
                            }
                            self.infos.append(fd_info)
                        elif target.startswith("/dev/shm/sem."):
                            fd_info = {
                                "fd": entry.name,
                                "caminho": target,
                                "tipo": "mutex"
                            }
                            self.infos.append(fd_info)
                        elif "anon_inode:mutex" in target:
                            fd_info = {
                                "fd": entry.name,
                                "caminho": target,
                                "tipo": "mutex"
                            }
                            self.infos.append(fd_info)
                        elif target.startswith("anon_inode:"):
                            fd_info = {
                                "fd": entry.name,
                                "caminho": target,
                                "tipo": "outro"
                            }
                            self.infos.append(fd_info)
                    except Exception:
                        continue

    def carregar_detalhes_processo(self):
        self.infos.clear()
        self.carregar_infos()
        return self.infos

