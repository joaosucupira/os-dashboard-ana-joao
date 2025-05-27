import os
from utils.util_diretorio import GerenciadorDiretorio, uid_para_nome

class DetalhesProcesso:
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
                                thread_info["state"] = line.split()[1]

                except Exception:
                    thread_info["name"] = "?"
                    thread_info["state"] = "?"

                self.threads_info.append(thread_info)

    def get_info_threads(self): 
        return self.threads_info
    
    def carregar_detalhes_processo(self):
        detalhes = {}
        status_path = f"{self.proc_dir}/status"
        stat_path = f"{self.proc_dir}/stat"
        cmdline_path = f"{self.proc_dir}/cmdline"

        # Nome, estado, usuário, prioridade, memória
        try:
            with open(status_path, "r") as f:
                for line in f:
                    if line.startswith("Name:"):
                        detalhes["nome"] = line.split()[1]
                    if line.startswith("State:"):
                        detalhes["estado"] = line.split()[1]
                    if line.startswith("Uid:"):
                        uid = line.split()[1]
                        detalhes["usuario"] = uid_para_nome(uid)
                    if line.startswith("VmRSS:"):
                        detalhes["memoria_kb"] = int(line.split()[1])
                    if line.startswith("Threads:"):
                        detalhes["threads"] = int(line.split()[1])
        except Exception:
            detalhes["nome"] = "?"
            detalhes["estado"] = "?"
            detalhes["usuario"] = "?"
            detalhes["memoria_kb"] = 0
            detalhes["threads"] = 0

        # Prioridade e tempo de CPU
        try:
            with open(stat_path, "r") as f:
                campos = f.read().split()
                prioridade = int(campos[17])
                tempo_usuario = int(campos[13])
                tempo_sistema = int(campos[14])
                total_t = tempo_usuario + tempo_sistema
                
                clk_tck = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
                detalhes["prioridade"] = prioridade
                detalhes["cpu_s"] = total_t / clk_tck

        except Exception:
            detalhes["prioridade"] = "?"
            detalhes["cpu_s"] = 0.0

        # Porcentagem de CPU (simples, acumulado)
        # Para %CPU real, seria necessário comparar com o tempo total do sistema em dois momentos
        detalhes["cpu_percent"] = "N/A"  # Placeholder

        self.detalhes = detalhes
        return detalhes