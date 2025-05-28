import os
from utils.util_diretorio import GerenciadorDiretorio, uid_para_nome, state_id_para_nome


class GerenciadorDetalhesMemoria:
    def __init__(self, pid):
        self.pid = str(pid)
        self.proc_dir = f'/proc/{self.pid}'
        self.threads_info = []
        


    def carregar_threads(self):
        task_dir = f'{self.proc_dir}/task'
        with GerenciadorDiretorio(task_dir) as gd:
            for entry in gd:
                tid = entry.name

                if tid == "." or tid == ".." : continue 

                thread_info = {"tid": tid}
                status_path = f'{task_dir}/{tid}/status'

                try:
                    with open(status_path, "r") as f:
                        for line in f:

                            if line.startswith("Name:"):
                                thread_info["name"] = line.split()[1]
                            if line.startswith("State:"):
                                thread_info["state"] = state_id_para_nome(line.split()[1])

                except Exception:
                    thread_info["name"] = "?"
                    thread_info["state"] = "?"

                self.threads_info.append(thread_info)

    def get_info_threads(self): 
        return self.threads_info
    
    def carregar_detalhes_processo(self):
        self.carregar_threads()
        detalhes = {}
        status_path = f"{self.proc_dir}/status"
        smaps_path = f"{self.proc_dir}/smaps"

        # Nome, estado, usuário
        try:
            with open(status_path, "r") as f:
                for line in f:
                    if line.startswith("Name:"):
                        detalhes["nome"] = line.split()[1]
                    if line.startswith("State:"):
                        detalhes["estado"] = state_id_para_nome(line.split()[1])
                    if line.startswith("Uid:"):
                        uid = line.split()[1]
                        detalhes["usuario"] = uid_para_nome(uid)
                        #detalhes["usuario"] = uid_para_nome(uid)
                    
        except Exception:
            detalhes["nome"] = "?"
            detalhes["estado"] = "?"
            detalhes["usuario"] = "?"

        # Informações de memória
        try:
            with open(smaps_path, "r") as fsmaps:
                linhas = fsmaps.readlines()
                writable = False
                size = 0
                rss = 0
                swap = 0
                shared_clean = 0
                shared_dirty = 0
                writable_mem = 0

                for line in linhas:
                    campos = line.split()

                    if len(campos) > 1 and "w" in campos[1]:
                        writable = True
                        
                    if line.startswith("Size:"):
                        size += int(line.split()[1])

                        if writable:
                            writable_mem += int(line.split()[1])

                    elif line.startswith("Rss:"):
                        rss += int(line.split()[1])
                    elif line.startswith("Swap:"):
                        swap += int(line.split()[1])
                    elif line.startswith("Shared_Clean:"):
                        shared_clean += int(line.split()[1])
                    elif line.startswith("Shared_Dirty:"):
                        shared_dirty += int(line.split()[1])

                detalhes["mem_fis_tot"] = size/1000 # Memoria fisica total
                detalhes["rss"] = rss/1000 # Memoria fisica residente (memoria realmente utilizada)
                detalhes["mem_vir_tot"] = swap/1000 # Memoria virtual
                detalhes["mem_compartilhavel"] = (shared_clean + shared_dirty)/1000 
                detalhes["mem_gravavel"] = writable_mem/1000 # Memoria gravavel


        except Exception:
            detalhes["mem_fis_tot"] = 0 
            detalhes["rss"] = 0 
            detalhes["mem_vir_tot"] = 0 
            detalhes["mem_compartilhavel"] = 0 
            detalhes["mem_gravavel"] = 0 

        self.detalhes = detalhes
        return detalhes