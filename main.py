# Arquivo principal - Dashboard
# No diretorio raiz rode 'python3 main.py' ou 'python main.py'
from Models.GerenciadorMemoria import GerenciadorMemoria

def main():
    gm = GerenciadorMemoria()
    percentual_uso = gm.calculaPercentualUso()
    print(f"Percentual de uso da memória: {percentual_uso:.2f}%")
    
if __name__ == "__main__":
    main()