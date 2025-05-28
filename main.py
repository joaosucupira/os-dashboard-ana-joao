# Arquivo principal - Dashboard
# No diretorio raiz rode 'python3 main.py' ou 'python main.py'

from Controllers.PrincipalController import PrincipalController
# from Models.GerenciadorDetalhesMemoria import GerenciadorDetalhesMemoria

def main():
    
    pc = PrincipalController()
    pc.executar()

    # gdm = GerenciadorDetalhesMemoria(1)  # Exemplo com PID 1 (init)
    # dic = gdm.carregar_detalhes_processo()

    # print(f"Nome: {dic.get('nome', '?')}, PID: {gdm.pid}, Usuário: {dic.get('usuario', '?')}, Estado: {dic.get('estado', '?')}, Memória (KB): {dic.get('mem_fis_tot', '?')}")


if __name__ == "__main__":
    main()