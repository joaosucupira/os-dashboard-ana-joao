from utils.util_diretorio import GerenciadorDiretorio, get_page_size, get_clk_tck

class GerenciadorProcessosMemoria:
    def listar_processos_e_usuarios(self):
        # Lista de processos que na realidade consiste em uma lista de dicionarios,
        # onde cada dicionario contem as informacoes de um processo.
        processos = []

        # Tamanho da pagina e clock ticks por segundo (precisa estudar melhor isso)
        page_t = get_page_size()
        clk_tck = get_clk_tck()

        
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
                        
                        # Dados a serem lidos do arquivo stat:
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
                                if line.startswith("Uid:"):
                                    uid = line.split()[1]

                        # Acessa o arquivo status para obter o nome do processo e o UID
                        # que sera convertido para o nome do usuario
                        # with open(smaps_rollup_path, "r") as fstatus:
                        #     linhas = fstatus.readlines()
                        #     name = None
                        #     uid = None
                        #     for line in linhas:
                        #         if line.startswith("Name:"):
                        #             name = line.split()[1].strip("()")
                        #         if line.startswith("Uid:"):
                        #             uid = line.split()[1]
                            

                        if uid is not None:
                            usuario = self.uid_para_nome(uid)

                            processos.append({
                                "pid": pid,
                                "nome": name,
                                "usuario": usuario,
                                
                            })
                    except Exception:
                        print(f"Erro ao ler processo {pid}: {entry.name}")
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