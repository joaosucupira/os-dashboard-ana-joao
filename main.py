# Arquivo principal - Dashboard
# No diretorio raiz rode 'python3 main.py' ou 'python main.py'

from Controllers.PrincipalController import PrincipalController
from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria

def main():
    # gpm = GerenciadorProcessosMemoria()
    # processos = gpm.listar_processos_e_usuarios()
    # for processo in processos:
    #     print(f"PID: {processo['pid']}, Nome: {processo['nome']}, Usuário: {processo['usuario']}\nMemória Alocada (kB): {processo['memoria_alocada_kb']}, Páginas: {processo['memoria_alocada_paginas']}\nPaginas de Código: {processo['codigo_paginas']}, Páginas de Heap: {processo['heap_paginas']}, Páginas de Stack: {processo['stack_paginas']}\n\n")
    
    pc = PrincipalController()
    pc.executar()

if __name__ == "__main__":
    main()