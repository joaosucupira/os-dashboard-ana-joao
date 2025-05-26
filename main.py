# Arquivo principal - Dashboard
# No diretorio raiz rode 'python3 main.py' ou 'python main.py'

from Controllers.PrincipalController import PrincipalController
from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria
# from Models.GerenciadorMemoria import GerenciadorMemoria

# import os # A biblioteca 'os' é necessária para clear_screen
# from time import sleep

# def clear_screen():
#     """Limpa o terminal. 'cls' para Windows, 'clear' para macOS/Linux."""
#     os.system('cls' if os.name == 'nt' else 'clear')

def main():
    gpm = GerenciadorProcessosMemoria()
    processos = gpm.listar_processos_e_usuarios()
    for processo in processos:
        print(f"PID: {processo['pid']}, Nome: {processo['nome']}, Usuário: {processo['usuario']}, ")
    
    # pc = PrincipalController()
    # pc.executar()
    

    # gm = GerenciadorMemoria()
    
    # while True:
    #     clear_screen()
    #     gm.atualizaDados()

    #     print("Memoria Ram:")
    #     print(f"{gm.calculaMemoriaFisicaUsada():.2f} GB ({gm.calculaPercentualUsoReal():.2f}%) de {gm.getMemoriaFisicaTotal():.2f} GB\n")

    #     sleep(1)
    
if __name__ == "__main__":
    main()