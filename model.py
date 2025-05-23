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

# Classe implementando uma struct C ... de processos individuais

class EstatisticasProcesso(Structure):
    _fields_ = [
        ("pid", c_ulong), # Inteiro sem sinal identificador do processo
        ("name", c_char * 256), # 
        ("status", c_char * 64), # Suspensa, Terminada, Executando...
        ("user", c_char * 128), 
        ("qtd_threads", c_ulong)
    ]

# CLASSES PYTHON

@dataclass
class Processo:
    pid: int
    name: str
    user: str

class Thread:
    def __init__(self):
        pass

# class System:
#     def __init__(self, t_atividade, ram_total, ram_disponivel, n_processos, )

# class System(Structure):
#     _fields_ = [
#         ("uptime", c_long), 
#         ("totalram", c_ulong),
#         ("freeram", c_ulong),
#         ("totalprocessos", c_ulong),
#         ("totalthreads", c_ulong)
#     ]

class UsoCPU(Structure):
    _fields_ = [
        ("usopercent", c_float),
        ("ociosopercent", c_float)

    ]

class Thread(Structure):
    _fields_ = [
        ("TID", c_ulong),
        ("processoPai", c_ulong),
        ("status", c_char * 64),
        ("CPU", c_float)
    ]

# Classe principal
class Model:
    def __init__(self):
        pass
