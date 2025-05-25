# Arquivo utilitario focado em manipulações de diretórios utilizando a bibliteca padrao C

import ctypes
import ctypes.util
from dataclasses import dataclass
from typing import Iterator

_SC_PAGESIZE = 30
_SC_CLK_TCK = 2

# Classe base que simula uma struct C que representa uma entrada de diretório.
# Usada para interagir com o sistema de arquivos em nível de sistema operacional.

class StructDir(ctypes.Structure):
    _fields_ = [
        ("d_ino", ctypes.c_ulong),      
        ("d_off", ctypes.c_ulong),      
        ("d_reclen", ctypes.c_ushort),  
        ("d_type", ctypes.c_ubyte),     
        ("d_name", ctypes.c_char * 256) 
    ]

# Classe de dados que adapta a estrutura de diretório para Python.

@dataclass
class DataDir:
    ino:    int
    off:    int
    reclen: int
    type:   int
    name:   str

class GerenciadorDiretorio:
    def __init__(self, path: str):
        self.libc = ctypes.CDLL(None)
        self.config_libc(path)
        
        
    # Configuração de abertura, leitura e fechamento dos diretórios.
    def config_libc(self, path):
        self.libc.opendir.argtypes = [ctypes.c_char_p]
        self.libc.opendir.restype = ctypes.c_void_p
        
        self.libc.readdir.argtypes = [ctypes.c_void_p]
        self.libc.readdir.restype = ctypes.POINTER(StructDir)
        
        self.libc.closedir.argtypes = [ctypes.c_void_p]
        self.libc.closedir.restype = ctypes.c_int
        
        self._dirp = self.libc.opendir(path.encode("utf-8"))
    
    # Iterador de diretorios
    def __iter__(self) -> Iterator[DataDir]:
        return self._iter_entries()

    # Lógica do iterador
    def _iter_entries(self):
        while True:
            dirent_p = self.libc.readdir(self._dirp)
            if not dirent_p:
                break
            conteudo = dirent_p.contents
            name = conteudo.d_name.decode("utf-8").rstrip("\x00")
            
            # Instancia o DataDir com os conteudos obtidos do diretorio
            yield DataDir(
                ino    = conteudo.d_ino,
                off    = conteudo.d_off,
                reclen = conteudo.d_reclen,
                type   = conteudo.d_type,
                name   = name
            )

    def close(self):
        if self._dirp:
            self.libc.closedir(self._dirp)
            self._dirp = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


# Funções uteis

def get_page_size():
    libc = ctypes.CDLL(None)
    return libc.sysconf(_SC_PAGESIZE)

def get_clk_tck():
    libc = ctypes.CDLL(None)
    return libc.sysconf(_SC_CLK_TCK)

