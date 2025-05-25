class GerenciadorMemoria:
    def calculaPercentualUso(self):
        """
        Calcula o percentual de uso da memória.
        """
        # Leitura do arquivo /proc/meminfo
        with open("/proc/meminfo", "r") as f:
            linhas = f.readlines()
        
        # Inicializa os valores de MemTotal e MemFree
        mem_total = 0
        mem_free = 0
        
        # Processa cada linha do arquivo
        for linha in linhas:
            if "MemTotal" in linha:
                mem_total = int(linha.split()[1])
            elif "MemFree" in linha:
                mem_free = int(linha.split()[1])
        
        # Cálculo do percentual de uso da memória
        if mem_total > 0:
            percentual_uso = ((mem_total - mem_free) / mem_total) * 100
            return percentual_uso
        
        return 0.0