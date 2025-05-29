from utils.util_diretorio import GerenciadorDiretorio, get_page_size, get_clk_tck
import os

class GerenciadorProcessosMemoria:
    def listar_processos_e_usuarios(self):
        # Lista de processos que na realidade consiste em uma lista de dicionarios,
        # onde cada dicionario contem as informacoes de um processo.
        processos = []

        # Tamanho da pagina e clock ticks por segundo (precisa estudar melhor isso)
        page_t = os.sysconf('SC_PAGE_SIZE') // 1024

        
        # Abre o gerenciador de diretorio para acessar o diretorio /proc
        with GerenciadorDiretorio("/proc") as gd:
            
            # Para cada entrada de /proc (que representa um processo ou arquivo de sistema),
            for entry in gd:
                
                # Checa se o nome da entrada eh um numero (pois apenas os processos sao numerados por PID)
                if entry.name.isdigit():

                    # Armazena o PID e os caminhos para os arquivos stat e status do processo
                    pid = entry.name
                    status_path = f"/proc/{pid}/status"
                    smaps_path = f"/proc/{pid}/smaps"
                    
                    # Try exception para abertura dos arquivos stat e status
                    try:

                        # Acessa o arquivo status para obter o nome do processo e o UID
                        # que sera convertido para o nome do usuario
                        with open(status_path, "r") as fstatus:
                            linhas = fstatus.readlines()
                            name = None
                            uid = None
                            mem_alocada = 0
                            mem_alocada_pags = 0
                            pags_cod = 0
                            pags_stack = 0
                            pags_heap = 0

                            for line in linhas:
                                if line.startswith("Name:"):
                                    name = line.split()[1].strip("()")
                                elif line.startswith("Uid:"):
                                    uid = line.split()[1]
                                elif line.startswith("VmSize"):
                                    mem_alocada = int(line.split()[1])
                                    mem_alocada_pags = int(line.split()[1]) // (page_t)
                                elif line.startswith("VmExe"):
                                    pags_cod = int(line.split()[1]) // (page_t)
                                elif line.startswith("VmData"):
                                    pags_heap = int(line.split()[1]) // (page_t)
                                elif line.startswith("VmStk"):
                                    pags_stack = int(line.split()[1]) // (page_t)
            

                        if uid is not None:
                            usuario = self.uid_para_nome(uid)

                            processos.append({
                                "pid": pid,
                                "nome": name,
                                "usuario": usuario,
                                "memoria_alocada_kb": mem_alocada,
                                "memoria_alocada_paginas": mem_alocada_pags,
                                "codigo_paginas": pags_cod,
                                "heap_paginas": pags_heap,
                                "stack_paginas": pags_stack
                            })
                    except Exception as e:
                        continue

        # Ordena os processos pela quantidade de memória alocada em ordem decrescente
        processos.sort(key=lambda p: int(p['memoria_alocada_kb']), reverse=True)
        
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
