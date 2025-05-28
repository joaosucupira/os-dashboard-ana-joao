# Model especializado na coleta geral de processos de '/proc'

from utils.util_diretorio import GerenciadorDiretorio, get_page_size, get_clk_tck, uid_para_nome, state_id_para_nome

class GerenciadorProcessos:
    
    def listar_processos_e_usuarios(self):
        processos = []
        page_t = get_page_size()
        clk_tck = get_clk_tck()

        with GerenciadorDiretorio("/proc") as gd:
            for entry in gd:
                if entry.name.isdigit():
                    pid = entry.name

                    # caminho para acessar nome, estado, n de threads, tempo de cpu
                    stat_path = f"/proc/{pid}/stat" 
                    # caminho para acessar usuario do processo
                    status_path = f"/proc/{pid}/status"


                    try:
                        # Iterando stat
                        name, estado_id, threads, t_cpu = self.ler_stat(stat_path, clk_tck)
                        # Iterando status
                        uid = self.ler_uid(status_path)

                        if uid is not None:
                 
                            usuario = uid_para_nome(uid)
                            estado = state_id_para_nome(estado_id)
                            processos.append({
                                "pid": pid,
                                "nome": name,
                                "usuario": usuario,
                                "threads": threads,
                                "estado": estado,
                                "cpu_s": t_cpu
                            })
                    except Exception:
                        continue # ignora todos os diretorios que nao sao processos

        processos.sort(key=lambda p: (-p['cpu_s'], int(p['pid'])))        
        # o retorno será utlizados pelo controller interessado
        return processos 
    
    def ler_stat(self, stat_path, clk_tck):

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

        return name, estado_id, threads, t_cpu

    def ler_uid(self, status_path):
        with open(status_path, "r") as fstatus:
            uid = None
            for line in fstatus:
                if line.startswith("Uid:"):
                    uid = line.split()[1]
                    break
        return uid

