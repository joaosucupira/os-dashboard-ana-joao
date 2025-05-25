from utils.util_diretorio import GerenciadorDiretorio

class GerenciadorProcessos:
    def listar_processos_e_usuarios(self):
        processos = []
        
        # Auxilio do GerenciadorDiretorio para ler o diretório /proc
        with GerenciadorDiretorio("/proc") as gd:
            for entry in gd:
                if entry.name.isdigit():
                    pid = entry.name
                    status_path = f"/proc/{pid}/status"
                    try:
                        with open(status_path, "r") as f:
                            uid = None
                            threads = None
                            for line in f:
                                if line.startswith("Uid:"):
                                    uid = line.split()[1]
                                if line.startswith("Threads:"):
                                    threads = int(line.split()[1])
                                if line.startswith("Name"):
                                    name = line.split()[1]
                                # if uid is not None and threads is not None:
                                #     break
                        if uid is not None:
                            # Conversão do valor numério do uid para nome do usuário
                            usuario = self.uid_para_nome(uid)
                            processos.append({
                                "pid": pid,
                                "nome": name,
                                "usuario": usuario,
                                "threads": threads
                            })
                    except Exception:
                        continue
        # Ordeno a lista de processos em decrescente para mostrar os mais relevantes
        processos.sort(key=lambda p: int(p["pid"]), reverse=True)
        return processos

    # Conversão do unix ID para nome do usuário
    def uid_para_nome(self, uid):
        try:
            with open("/etc/passwd", "r") as passwd_file:
                for line in passwd_file:
                    partes = line.split(":")
                    if len(partes) > 2 and partes[2] == str(uid):
                        return partes[0]
        except Exception:
            pass
        return f"UID {uid}"

