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
                            if line.startswith("VmStk:"):
                                thread_info["vm_stack"] = int(line.split()[1])

                except Exception:
                    thread_info["name"] = "?"
                    thread_info["state"] = "?"
                    thread_info["vm_stack"] = 0

                self.threads_info.append(thread_info)

    def get_info_threads(self): 
        return self.threads_info
    
    def carregar_detalhes_processo(self):
        self.carregar_threads()
        detalhes = {}
        status_path = f"{self.proc_dir}/status"

        detalhes["mem_compartilhavel"] = 0

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
                    if line.startswith("RssAnon:"):
                        detalhes["mem_fis_tot"] = int(line.split()[1]) / 1024 # mB
                    if line.startswith("VmSize"):
                        detalhes["mem_vir_tot"] = int(line.split()[1]) / (1024*1024) # GB
                    if line.startswith("VmRSS:"):
                        detalhes["rss"] = int(line.split()[1]) / 1024 # mB
                    if line.startswith("RssFile"):
                        detalhes["mem_compartilhavel"] += int(line.split()[1]) / 1024
                    if line.startswith("RssShmem"):
                        detalhes["mem_compartilhavel"] += int(line.split()[1]) / 1024


                    
        except Exception:
            detalhes["nome"] = "?"
            detalhes["estado"] = "?"
            detalhes["usuario"] = "?"
            detalhes["mem_fis_tot"] = 0 
            detalhes["mem_vir_tot"] = 0
            detalhes["rss"] = 0 
            detalhes["mem_compartilhavel"] = 0 

        self.detalhes = detalhes
        return detalhes