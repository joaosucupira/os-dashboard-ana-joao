# util_diretorio.py (versão com leitura de caminhos e links atualizados)

import ctypes
import os
from dataclasses import dataclass
from typing import Iterator

# Classe base que simula uma struct C que representa uma entrada de diretório.
class StructDir(ctypes.Structure):
    _fields_ = [
        ("d_ino", ctypes.c_ulong),      
        ("d_off", ctypes.c_ulong),      
        ("d_reclen", ctypes.c_ushort),  
        ("d_type", ctypes.c_ubyte),     
        ("d_name", ctypes.c_char * 256) 
    ]

# Constantes para os tipos de arquivo do campo d_type.
DT_UNKNOWN = 0
DT_LNK = 10 # d_type para Link Simbólico (Symbolic Link)

# Classe de dados que adapta a estrutura de diretório para Python.
@dataclass
class DataDir:
    ino:    int
    off:    int
    reclen: int
    type:   int
    name:   str
    caminho: str # Armazena o caminho completo da entrada

    def is_symlink(self) -> bool:
        # Verifica se a entrada é um link simbólico, de forma otimizada e segura
        if self.type != DT_UNKNOWN:
            return self.type == DT_LNK
        try:
            return os.path.islink(self.caminho)
        except FileNotFoundError:
            return False

    def readlink(self) -> str:
        #Lê o destino de um link simbólico de forma segura
        try:
            return os.readlink(self.caminho)
        except (FileNotFoundError, OSError):
            return ""

class GerenciadorDiretorio:
    def __init__(self, path: str):
        self.path = path # Armazena o caminho do diretório
        self.libc = ctypes.CDLL(None)
        
        # Verifica se o caminho existe e é um diretório
        if not os.path.isdir(self.path):
            self._dirp = None
        else:
            self.config_libc(self.path)

    def config_libc(self, path):
        self.libc.opendir.argtypes = [ctypes.c_char_p]
        self.libc.opendir.restype = ctypes.c_void_p
        
        self.libc.readdir.argtypes = [ctypes.c_void_p]
        self.libc.readdir.restype = ctypes.POINTER(StructDir)
        
        self.libc.closedir.argtypes = [ctypes.c_void_p]
        self.libc.closedir.restype = ctypes.c_int
        
        try:
            self._dirp = self.libc.opendir(path.encode("utf-8"))
        except Exception:
            self._dirp = None
    
    def __iter__(self) -> Iterator[DataDir]:
        # Não itera se o diretório não pôde ser aberto
        if not self._dirp:
            return iter(())
        return self._iter_entries()

    def _iter_entries(self):
        while True:
            dirent_p = self.libc.readdir(self._dirp)
            if not dirent_p:
                break
            conteudo = dirent_p.contents
            name = conteudo.d_name.decode("utf-8").rstrip("\x00")
            
            if name in ('.', '..'):
                continue

            caminho_completo = os.path.join(self.path, name)
            
            yield DataDir(
                ino    = conteudo.d_ino,
                off    = conteudo.d_off,
                reclen = conteudo.d_reclen,
                type   = conteudo.d_type,
                name   = name,
                caminho = caminho_completo
            )

    def close(self):
        if self._dirp:
            self.libc.closedir(self._dirp)
            self._dirp = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

# A partir daqui o codigo nao foi alterado
# Funções uteis

# Indices para parametro de sistemas da função c 'sysconf' para obter respectivamente
# o tamanho da pagina e o clock ticks por segundo

_SC_PAGESIZE = 30
_SC_CLK_TCK = 2

def get_page_size():
    libc = ctypes.CDLL(None)
    return libc.sysconf(_SC_PAGESIZE)

def get_clk_tck():
    libc = ctypes.CDLL(None)
    return libc.sysconf(_SC_CLK_TCK)

def uid_para_nome(uid):
    try:
        with open("/etc/passwd", "r") as passwd_file:
            for line in passwd_file:
                partes = line.split(":")
                if len(partes) > 2 and partes[2] == str(uid):
                    return partes[0]
    except Exception:
        pass
    return f"UID {uid}"

def state_id_para_nome(state_id):
    estados = {
        "R": "Executando",
        "S": "Dormindo",
        "D": "Travado",
        "Z": "Zumbi",
        "T": "Parado",
        "t": "Parado (rastre.)",
        "X": "Morto",
        "x": "Morto",
        "K": "Destruído",
        "W": "Paginação",
        "P": "Parado+",
        "I": "Ocioso"
    }
    # Pode ocorrer do estado Dormindo ser interpretado incorretamente, verifique o estado no proprio proc
    return estados.get(state_id, "Desconhecido")