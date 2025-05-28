# Model especializado na coleta geral de processos de '/proc'

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

                    # caminho para acessar nome, estado, n de threads, tempo de cpu e memoria
                    stat_path = f"/proc/{pid}/stat" 
                    # caminho para acessar usuario do processo
                    status_path = f"/proc/{pid}/status"


                    try:
                        # Iterando stat
                        name, estado_id, threads, t_cpu, memoria_kb = self.ler_stat(stat_path, clk_tck, page_t)
                        # Iterando status
                        uid = self.ler_uid(status_path)

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
                        continue # ignora todos os diretorios que nao sao processos

        # ordenanado os processos de acordo com 3 critérios principais
        processos.sort(key=lambda p: (-p['cpu_s'], -p['mem_kb'], int(p['pid'])))        
        # o retorno será utlizados pelo controller interessado
        return processos 
    
    def ler_stat(self, stat_path, clk_tck, page_t):
        # Campos referenciando os respectivos índices do arquivo inline que contém o que precisamos
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
            memoria_kb = (rss * page_t) / (1024)
        return name, estado_id, threads, t_cpu, memoria_kb

    def ler_uid(self, status_path):
        with open(status_path, "r") as fstatus:
            uid = None
            for line in fstatus:
                if line.startswith("Uid:"):
                    uid = line.split()[1]
                    break
        return uid

    # conversão do uid pra o nome do usuario
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
        # Pode ocorrer do estado Dormindo ser interpretado incorretamente, verifique o estado no proprio proc
        return estados.get(state_id, "Desconhecido")