from utils.util_diretorio import GerenciadorDiretorio, get_page_size, get_clk_tck
import os

class GerenciadorProcessosMemoria:
    def listar_processos_e_usuarios(self):
        # Lista de processos que na realidade consiste em uma lista de dicionarios,
        # onde cada dicionario contem as informacoes de um processo.
        processos = []

        # Tamanho da pagina e clock ticks por segundo (precisa estudar melhor isso)
        page_t = os.sysconf('SC_PAGE_SIZE')

        
        # Abre o gerenciador de diretorio para acessar o diretorio /proc
        with GerenciadorDiretorio("/proc") as gd:
            
            # Para cada entrada de /proc (que representa um processo ou arquivo de sistema),
            for entry in gd:
                
                # Checa se o nome da entrada eh um numero (pois apenas os processos sao numerados por PID)
                if entry.name.isdigit():

                    # Armazena o PID e os caminhos para os arquivos stat e status do processo
                    pid = entry.name
                    status_path = f"/proc/{pid}/status"
                    smaps_rollup_path = f"/proc/{pid}/smaps_rollup"
                    smaps_path = f"/proc/{pid}/smaps"
                    
                    # Try exception para abertura dos arquivos stat e status
                    try:
                        
                        # Dados a serem lidos:
                        # - PID, // status
                        # - nome do processo, //status
                        # - usuario, // definido no 2o with, mas eh no status
                        # - quantidade total de memória alocada,  //smaps_rollup -> Pss (ideal) ou status -> VmRSS
                        # - quantidade de páginas de memória( //smap
                            # - total, //smaps_rollup -> Rss (ideal) (em kB, precisa ser convertido p/ qtdd. de pags.)
                            # - de código, // smaps -> para cada VMA do processo que eh executavel e com permissao de execucao
                            #              // somar o valor do campo Pss e converter de kB para quantidade de paginas
                            # - heap, // smaps -> para cada VMA do processo que eh identificado como [heap] 
                            #         // somar o valor do campo Pss e converter de kB para quantidade de paginas
                            # - stack // smaps -> para cada VMA do processo que eh identificado como [heap] 
                            #         // somar o valor do campo Pss e converter de kB para quantidade de paginas
                        # )

                        # Acessa o arquivo status para obter o nome do processo e o UID
                        # que sera convertido para o nome do usuario
                        with open(status_path, "r") as fstatus:
                            linhas = fstatus.readlines()
                            name = None
                            uid = None
                            

                            for line in linhas:
                                if line.startswith("Name:"):
                                    name = line.split()[1].strip("()")
                                elif line.startswith("Uid:"):
                                    uid = line.split()[1]
            

                        # Acessa o arquivo smaps_rollup para obter
                        # a quantidade total de memória alocada e a quantidade total de páginas de memoria
                        # with open(smaps_rollup_path, "r") as fsmaps_rollup:
                        #     linhas = fsmaps_rollup.readlines()
                            
                        #     for line in linhas:
                        #         if line.startswith("Size:"):
                        #             size = int(line.split()[1])

                        # Acessa o arquivo smaps para obter quantidade de páginas de memória alocada, de heap e de stack
                        # Percorrendo todos os VMAs do processo em questao
                            # VMA = mapeamentos de memória virtual (VMAs - Virtual Memory Areas)
                            # Os processos tem varias areas de memoria virtual, cada uma com suas caracteristicas
                            # e permissões, como código executável, heap, stack, etc.
    
                        with open(smaps_path, "r") as fsmaps:
                            linhas = fsmaps.readlines()
                            size = 0
                            code_pages = 0
                            heap_pages = 0
                            stack_pages = 0
                            current_vma = None  # Variável para rastrear a VMA atual

                            for line in linhas:
                                campos = line.split()
                                # Transforma a linha em uma lista de campos
                                
                                # Analisa o segundo campo da linha que corresponde as permissões da VMA
                                if len(campos) > 1 and "x" in campos[1]:
                                    # Se a VMA tem permissão de execução, soma as páginas de código
                                    current_vma = "code"

                                elif "[heap]" in line:
                                    # Se a linha contém [heap], indica o início da área de heap
                                    current_vma = "heap"

                                elif "[stack]" in line:
                                    # Se a linha contém [stack], indica o início da área de stack
                                    current_vma = "stack"

                                elif current_vma == "code" and line.startswith("Size:"):
                                    # Se a linha contém Pss e estamos na área de código, soma a memoria de código
                                    code_pages += int(line.split()[1])

                                elif current_vma == "heap" and line.startswith("Size:"):
                                    # Se a linha contém Pss e estamos na área de heap, soma a memoria de heap
                                    heap_pages += int(line.split()[1])

                                elif current_vma == "stack" and line.startswith("Size:"):
                                    # Se a linha contém Pss e estamos na área de stack, soma a memoria de stack
                                    stack_pages += int(line.split()[1])

                                elif line.startswith("Size:"):
                                    # Se a linha contém Size, indica o tamanho total da memória alocada
                                    size += int(line.split()[1])

                        if uid is not None:
                            usuario = self.uid_para_nome(uid)

                            processos.append({
                                "pid": pid,
                                "nome": name,
                                "usuario": usuario,
                                "memoria_alocada_kb": size,
                                "memoria_alocada_paginas": size // page_t,
                                "codigo_paginas": code_pages // page_t,
                                "heap_paginas": heap_pages // page_t,
                                "stack_paginas": stack_pages // page_t
                            })
                    except Exception as e:
                        print(f"Erro ao processar PID {pid}: {e}")
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