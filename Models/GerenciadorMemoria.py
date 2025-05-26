class GerenciadorMemoria:
    
    def __init__(self):
        """
        Inicializa o gerenciador de memória.
        """
        # Leitura do arquivo /proc/meminfo
        with open("/proc/meminfo", "r") as f:
            linhas = f.readlines()

        self.mem_total = 0
        self.mem_free = 0
        self.mem_available = 0
        self.swap_total = 0
        self.swap_free = 0
        self.cached = 0
        
        self.dados_memoria = {}
        self.dados_memoria = self.atualizaDados()

    # Obs: colocar isso aqui em uma thread la no controler
    def atualizaDados(self):
        """
        Atualiza os dados de memória lendo novamente o arquivo /proc/meminfo.
        """
        with open("/proc/meminfo", "r") as f:
            linhas = f.readlines()

        for linha in linhas:
            if "MemTotal" in linha:
                self.mem_total = int(linha.split()[1])
            elif "MemFree" in linha:
                self.mem_free = int(linha.split()[1])
            elif "MemAvailable" in linha:
                self.mem_available = int(linha.split()[1])
            elif "SwapTotal" in linha:
                self.swap_total = int(linha.split()[1])
            elif "SwapFree" in linha:
                self.swap_free = int(linha.split()[1])
            elif "Cached" in linha:
                self.cached = int(linha.split()[1])

        # Dicionario contendo apenas os dados que serao mostrados em tela
        # Para memória física (RAM) e virtual (SWAP):
        # percentual de uso da memória (real),
        # quantidade usada,
        # quantidade total,
        # percentual de memória livre (real),
        # cache

        self.dados_memoria = {
            # Dados de memória física (RAM)
            "mem_total": self.getMemoriaFisicaTotal(),
            "mem_use_perc": self.calculaPercentualUso(),
            "mem_used": self.calculaMemoriaFisicaUsada(),
            # Dados de memória virtual (SWAP)
            "swap_total": self.getMemoriaVirtualTotal(),
            "swap_use_perc": self.calculaPercentualMemoriaVirtualUsada(),
            "swap_used": self.calculaMemoriaVirtualUsada(),
            # Memoria cache
            "cached": self.getCache()
        }

        return self.dados_memoria

    
    def getMemoriaFisicaTotal(self):
        # Retorna a quantidade total de memória física (RAM) em GB.
        
        return self.mem_total / 1000000  # Convertendo de KB para GB

    def getMemoriaFisicaLivre(self):
        # Retorna a quantidade total de memória física (RAM) livre em GB.
        
        return self.mem_free / 1000000

    def getMemoriaFisicaDisponivel(self):
        # Retorna a quantidade total de memória física (RAM) disponível em GB,
        # desconsiderando a memoria dedica a buffers e cache.
        
        return self.mem_available / 1000000

    def getMemoriaVirtualTotal(self):
        # Retorna a quantidade total de memória virtual (SWAP) em GB.

        return self.swap_total/ 1000000

    def getMemoriaVirtualLivre(self):
        # Retorna a quantidade total de memória virtual (SWAP) livre em GB.
        
        return self.swap_free / 1000000

    def getCache(self):
        # Retorna a quantidade total de memória cache em GB.
        
        return self.cached / 1000000

    def calculaPercentualUso(self):
        # Cálculo do percentual de uso da memória com base em memória disponivel.

        if self.mem_total > 0:
            percentual_uso = (self.calculaMemoriaFisicaUsada() / self.mem_total) * 100
            return percentual_uso
        
        return 0.0

    def calculaPercentualMemoriaDisponivel(self):
        # Cálculo do percentual de memória fisica (RAM) disponível (aquela que desconsidera buffers e cache).

        if self.mem_total > 0:
            percentual_memoria_disponivel = (self.mem_available / self.mem_total) * 100
            return percentual_memoria_disponivel
        
        return 0.0

    def calculaMemoriaFisicaUsada(self):
        # Calcula a quantidade de memória física (RAM) usada em GB.
        
        return (self.mem_total - self.mem_available) / 1000000

    def calculaMemoriaVirtualUsada(self):
        # Calcula a quantidade de memória virtual (SWAP) usada em GB.
        
        return (self.swap_total - self.swap_free) / 1000000

    def calculaPercentualMemoriaVirtualUsada(self):
        # Cálculo do percentual de memória virtual usada em GB.

        swap_usado = self.calculaMemoriaVirtualUsada()
        if swap_usado > 0:
            percentual_memoria_virtual_usada = (swap_usado / self.swap_total) * 100
            return percentual_memoria_virtual_usada
        
        return 0.0
