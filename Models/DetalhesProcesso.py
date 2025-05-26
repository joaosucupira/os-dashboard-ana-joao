from utils.util_diretorio import GerenciadorDiretorio

class DetalhesProcesso:
    def __init__(self, pid):
        self.pid = str(pid)
        self.proc_dir = f'/proc/{self.pid}'
        self.threads_info = []
        self.carregar_threads()


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

    def get_info_threads(self): return self.threads_info