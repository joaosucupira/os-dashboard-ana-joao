# Arquivo principal - Dashboard
# No diretorio raiz rode 'python3 main.py' ou 'python main.py'

from Controllers.PrincipalController import PrincipalController
from Views.DetalhesProcessoView import DetalhesProcessoView
from Models.DetalhesProcesso import DetalhesProcesso
import customtkinter as ctk

def main():
    pc = PrincipalController()
    pc.executar()

if __name__ == "__main__":
    main()