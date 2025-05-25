# Arquivo principal - Dashboard
# No diretorio raiz rode 'python3 main.py' ou 'python main.py'
from Models.GerenciadorMemoria import GerenciadorMemoria

import os # A biblioteca 'os' é necessária para clear_screen
from time import sleep

def clear_screen():
    """Limpa o terminal. 'cls' para Windows, 'clear' para macOS/Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    gm = GerenciadorMemoria()
    
    while True:
        clear_screen()
        gm.atualizaDados()

        print("Memoria Ram:")
        print(f"{gm.calculaMemoriaFisicaUsada():.2f} GB ({gm.calculaPercentualUsoReal():.2f}%) de {gm.getMemoriaFisicaTotal():.2f} GB\n")

        sleep(1)
    
if __name__ == "__main__":
    main()