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
    https://www.youtube.com/watch?time_continue=56&v=ImfyJ_AC9DY&embeds_referring_euri=https%3A%2F%2Fchatgpt.com%2F&source_ve_path=MTM5MTE3LDEzOTExNywxMjcyOTksMjg2NjY