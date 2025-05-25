class GerenciadorMemoria:
    
    def __init__(self):
        """
        Inicializa o gerenciador de memória.
        """
        # Leitura do arquivo /proc/meminfo
        with open("/proc/meminfo", "r") as f:
            linhas = f.readlines()

        # Inicializa os valores de MemTotal, MemFree, MemAvailable, SwapTotal e SwapFree
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
    
    def getMemoriaFisicaTotal(self):
        """
        Retorna a quantidade total de memória física em GB.
        """
        
        return self.mem_total / 1000000  # Convertendo de KB para GB

    def getMemoriaFisicaLivre(self):
        """
        Retorna a quantidade total de memória física livre em GB.
        """
        
        return self.mem_free / 1000000

    def getMemoriaFisicaDisponivel(self):
        """
        Retorna a quantidade total de memória física disponível em GB.
        """
        
        return self.mem_available / 1000000

    def getMemoriaVirtualTotal(self):
        """
        Retorna a quantidade total de memória virtual em GB.
        """
        return self.swap_total/ 1000000

    def getMemoriaVirtualLivre(self):
        """
        Retorna a quantidade total de memória virtual livre em GB.
        """
        return self.swap_free / 1000000



        """
        Retorna a quantidade de memória cache em GB.
        """
        
        return self.cached / 1000000

    def getCache(self):
        """
        Retorna a quantidade de memória cache em GB.
        """
        
        return self.cached / 1000000

    def calculaPercentualUso(self):
        """
        Calcula o percentual de uso da memória fisica. Esse calculo considera memoria dedicada a buffers e caches
        """
        # Cálculo do percentual de uso da memória
        if self.mem_total > 0:
            percentual_uso = (self.calculaMemoriaFisicaUsada / self.mem_total) * 100
            return percentual_uso
        
        return 0.0

    def calculaPercentualUsoReal(self):
        """
        Calcula o percentual de uso da memória fisica desconsiderando memoria dedica a cache e buffers.
        """
        # Esse calculo eh dito mais realista no sentido de que considera toda a memória disponível,
        # incluindo buffers e caches, para calcular o percentual de uso da memória.

        # Cálculo do percentual de uso da memória
        if self.mem_total > 0:
            percentual_uso_real = ((self.mem_total - self.mem_available) / self.mem_total) * 100
            return percentual_uso_real
        
        return 0.0

    def calculaPercentualMemoriaLivre(self):
        """
        Calcula o percentual de memória fisica livre.
        """
        
        # Cálculo do percentual de memória livre
        if self.mem_total > 0:
            percentual_memoria_livre = (self.mem_free / self.mem_total) * 100
            return percentual_memoria_livre
        
        return 0.0

    def calculaPercentualMemoriaDisponivel(self):
        """
        Calcula o percentual de memória fisica disponível.
        """

        # Cálculo do percentual de memória disponível
        if self.mem_total > 0:
            percentual_memoria_disponivel = (self.mem_available / self.mem_total) * 100
            return percentual_memoria_disponivel
        
        return 0.0

    def calculaMemoriaFisicaUsada(self):
        """
        Calcula a quantidade de memória física usada em GB.
        """
        
        return (self.mem_total - self.mem_available) / 1000000

    def calculaMemoriaVirtualUsada(self):
        """
        Calcula a quantidade de memória virtual usada em GB.
        """
        
        return (self.swap_total - self.swap_free) / 1000000

    def calculaPercentualMemoriaVirtualUsada(self):
        """
        Calcula o percentual de memória virtual usada.
        """
        
        # Cálculo do percentual de memória virtual usada
        swap_usado = calculaMemoriaVirtualUsada()
        if swap_usado > 0:
            percentual_memoria_virtual_usada = (swap_usado / self.swap_total) * 100
            return percentual_memoria_virtual_usada
        
        return 0.0
