from utils.util_diretorio import GerenciadorDiretorio, get_page_size, get_clk_tck, uid_para_nome

class GerenciadorProcessos:
    def listar_processos_e_usuarios(self):
        processos = []
        page_t = get_page_size()
        clk_tck = get_clk_tck()

        with GerenciadorDiretorio("/proc") as gd:
            for entry in gd:
                if entry.name.isdigit():

                    pid = entry.name
                    stat_path = f"/proc/{pid}/stat"
                    status_path = f"/proc/{pid}/status"
                    try:
                        
                        with open(stat_path, "r") as fstat:
                            campos = fstat.read().split()
                            name = campos[1].strip("()")
                            estado_id = campos[2]
                            threads = int(campos[19])
                            tempo_usuario = int(campos[13])
                            tempo_sistema = int(campos[14])
                            total_t = tempo_usuario + tempo_sistema
                            t_cpu = total_t / clk_tck
                            rss = int(campos[23])
                            memoria_kb = (rss * page_t) // 1024
                        
                        with open(status_path, "r") as fstatus:
                            uid = None
                            for line in fstatus:
                                if line.startswith("Uid:"):
                                    uid = line.split()[1]
                                    break

                        if uid is not None:
                            usuario = uid_para_nome(uid)
                            estado = self.state_id_para_nome(estado_id)

                            processos.append({
                                "pid": pid,
                                "nome": name,
                                "usuario": usuario,
                                "threads": threads,
                                "estado": estado,
                                "cpu_s": t_cpu,
                                "mem_kb": memoria_kb
                            })
                    except Exception:
                        continue
        processos.sort(key=lambda p: (-p['cpu_s'], -p['mem_kb'], int(p['pid'])))        
        return processos
    
    def state_id_para_nome(self, state_id):

        estados = {
            "R": "Executando",
            "S": "Dormindo",
            "D": "Travado",
            "Z": "Zumbi",
            "T": "Parado",
            "t": "Parado (rastre.)",
            "X": "Morto",
            "x": "Morto",
            "K": "Destruído",
            "W": "Paginação",
            "P": "Parado+",
            "I": "Ocioso"
        }
        return estados.get(state_id, "Desconhecido")

    def carregar_detalhes_processo(self, pid):
        detalhes = {}
        status_path = f"{pid}/status"
        stat_path = f"{pid}/stat"

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

        try:
            with open(stat_path, "r") as f:
                campos = f.read().split()
                prioridade = int(campos[17])
                tempo_usuario = int(campos[13])
                tempo_sistema = int(campos[14])
                total_t = tempo_usuario + tempo_sistema
                
                clk_tck = get_clk_tck()
                detalhes["prioridade"] = prioridade
                detalhes["cpu_s"] = total_t / clk_tck

        except Exception:
            detalhes["prioridade"] = "?"
            detalhes["cpu_s"] = 0.0

        detalhes["cpu_percent"] = "N/A" 

        return detalhes