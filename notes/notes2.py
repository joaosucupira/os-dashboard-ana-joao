import ctypes
import os 

# Joao: cada instancia dessa classe é uma dll carregada/biblioteca compartilhada 
# padrão C
libc = ctypes.CDLL(None)

libc.fork.restype = ctypes.c_int

cfork = libc.fork

if cfork == 0:
    print("processo filho")
else:
    print(f'processo pai, filho {cfork}')
