# Gerenciador voltado para informações gerais do processador

import time
from Models.GerenciadorProcessos import GerenciadorProcessos

class GerenciadorCPU:
    def __init__(self):
        self.last_total = 0
        self.last_idle = 0

    def ler_cpu(self):
        with open("/proc/stat") as f:
            campos = f.readline().split()
            total = sum(map(int, campos[1:]))
            idle = int(campos[4])
        return total, idle

    def calcular_percentuais(self):
        total1, idle1 = self.ler_cpu()
        time.sleep(0.1)
        total2, idle2 = self.ler_cpu()
        total_diff = total2 - total1
        idle_diff = idle2 - idle1
        uso = 100 * (total_diff - idle_diff) / total_diff if total_diff else 0
        ocioso = 100 * idle_diff / total_diff if total_diff else 0
        return round(uso, 2), round(ocioso, 2)

    def contar_processos_threads(self):
        gp = GerenciadorProcessos()
        processos = gp.listar_processos_e_usuarios()
        total_threads = sum(p['threads'] for p in processos)
        return len(processos), total_threads