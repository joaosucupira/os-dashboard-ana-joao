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
                            for line in f:
                                if line.startswith("Uid:"):
                                    uid = line.split()[1]
                                    break
                        if uid is not None:
                            # Busca o nome do usuário manualmente em /etc/passwd
                            usuario = self.uid_para_nome(uid)
                            processos.append({"pid": pid, "usuario": usuario})
                    except Exception:
                        continue
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

