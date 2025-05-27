# Arquivo principal - Dashboard
# No diretorio raiz rode 'python3 main.py' ou 'python main.py'

from Controllers.PrincipalController import PrincipalController
from Models.DetalhesProcesso import DetalhesProcesso

def main():
    pc = PrincipalController()
    pc.executar()
    # dp = DetalhesProcesso(3386)
    # info = dp.get_info_threads()
    # for thread in info:
    #     print(f"{thread['tid']} - {thread['name']} - {thread['state']}")
    

if __name__ == "__main__":
    main()