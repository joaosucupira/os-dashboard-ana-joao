import ctypes
import os
import subprocess # Para compilar nosso código C

# --- COMPILAÇÃO AUTOMÁTICA DO AJUDANTE C ---

# Caminho para o nosso código C e para a biblioteca compilada
c_helper_source = os.path.join(os.path.dirname(__file__), 'helper.c')
c_helper_lib = os.path.join(os.path.dirname(__file__), 'helper.so')

# Compila o helper.c em helper.so se a biblioteca não existir ou for mais antiga que o código-fonte
if not os.path.exists(c_helper_lib) or os.path.getmtime(c_helper_source) > os.path.getmtime(c_helper_lib):
    print("Compilando o ajudante C (helper.c)...")
    try:
        # Comando para compilar o código C em uma biblioteca compartilhada
        compile_command = ['gcc', '-shared', '-o', c_helper_lib, '-fPIC', c_helper_source]
        subprocess.run(compile_command, check=True)
        print("Ajudante compilado com sucesso.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"ERRO CRÍTICO: Falha ao compilar helper.c. Verifique se o 'gcc' está instalado.")
        print(f"Erro: {e}")
        # Se não conseguir compilar, o programa não pode continuar.
        exit(1)

# --- CARREGAMENTO DA NOSSA BIBLIOTECA C ---

# Carrega a biblioteca que acabamos de compilar
libc_helper = ctypes.CDLL(c_helper_lib)

# Define a estrutura Python que corresponde à nossa 'SimpleStat' em C
class SimpleStat(ctypes.Structure):
    _fields_ = [
        ('size', ctypes.c_longlong),
        ('mtime', ctypes.c_long),
        ('is_dir', ctypes.c_int),
        ('mode', ctypes.c_int),
    ]

# Prepara a função get_simple_stat da nossa biblioteca
get_simple_stat = libc_helper.get_simple_stat
get_simple_stat.argtypes = [ctypes.c_char_p, ctypes.POINTER(SimpleStat)]
get_simple_stat.restype = ctypes.c_int


# --- FUNÇÃO get_file_info (AGORA USANDO O AJUDANTE C) ---

def get_file_info(path):
    """
    Obtém informações de um arquivo chamando nossa função C compilada,
    que por sua vez usa a syscall stat.
    """
    stats = SimpleStat()
    path_bytes = path.encode('utf-8')
    
    # Chama a função do nosso helper C
    if get_simple_stat(path_bytes, ctypes.byref(stats)) != 0:
        return None

    # Converte as permissões para o formato octal (ex: '755')
    permissions = oct(stats.mode)[-3:]
    
    return {
        "size": stats.size,
        "is_dir": bool(stats.is_dir),
        "permissions": permissions,
        "mtime": stats.mtime,
    }

# --- CÓDIGO PARA PARTIÇÕES (PERMANECE O MESMO, POIS JÁ ESTAVA ESTÁVEL) ---

class struct_statvfs(ctypes.Structure):
    _fields_ = [
        ('f_bsize', ctypes.c_ulong), ('f_frsize', ctypes.c_ulong),
        ('f_blocks', ctypes.c_ulonglong), ('f_bfree', ctypes.c_ulonglong),
        ('f_bavail', ctypes.c_ulonglong), ('f_files', ctypes.c_ulonglong),
        ('f_ffree', ctypes.c_ulonglong), ('f_favail', ctypes.c_ulonglong),
        ('f_fsid', ctypes.c_ulong), ('f_flag', ctypes.c_ulong),
        ('f_namemax', ctypes.c_ulong), ('__f_spare', ctypes.c_int * 6),
    ]

libc = ctypes.CDLL(None)
statvfs = libc.statvfs
statvfs.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_statvfs)]
statvfs.restype = ctypes.c_int

def get_fs_usage(path):
    fs_stats = struct_statvfs()
    path_bytes = path.encode('utf-8')
    if statvfs(path_bytes, ctypes.byref(fs_stats)) != 0:
        return None
    total_gb = (fs_stats.f_blocks * fs_stats.f_frsize) / (1024**3)
    free_gb = (fs_stats.f_bfree * fs_stats.f_frsize) / (1024**3)
    used_gb = total_gb - free_gb
    use_perc = (used_gb / total_gb) * 100 if total_gb > 0 else 0
    return {"total": total_gb, "used": used_gb, "free": free_gb, "use_perc": use_perc}