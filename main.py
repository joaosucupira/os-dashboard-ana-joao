# Arquivo principal - Dashboard
# No diretorio raiz rode 'python3 main.py' ou 'python main.py'

from Models.GerenciadorProcessos import GerenciadorProcessos

def main():
    gp = GerenciadorProcessos()
    processos = gp.listar_processos_e_usuarios()
    for p in processos:
        print(f'PID:  {p['pid']} - Usuario:  {p['usuario']}')
if __name__ == "__main__":
    main()