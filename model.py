# A regra de negócio que modela os dados e define como se comportam 
# os elementos sem se preocupar com visualização e acesso

import ctypes
from ctypes import c_ulong, c_long, c_char, c_float, util, Structure

from dataclasses import dataclass
import os
from os import path

libc = ctypes.CDLL(None)


# NOTA: Nao precisa ser todas essas classes procura fazer o que o requisito pede e imprimir no console msm

# STRUCTS

# Classe implementando uma struct C para tratar dados brutos das chamadas de sistema
# em diretórios ou entradas de diretórios

class DiretorioEntrada(ctypes.Structure):
    _fields_ = [
        ("dirIno", ctypes.c_ulong), # id unico do diretorio
        ("dirNome", ctypes.c_char * 256),
        ("dirTipo", ctypes.c_ubyte), # tipo da entrada
        ("dirReclen", ctypes.c_ushort), # tamanho da entrada
        ("dirOff", ctypes.c_ulong), # offset/deslocamento p proxima entrada
    ]


# Classe principal
class Model:
    def __init__(self):
        pass
