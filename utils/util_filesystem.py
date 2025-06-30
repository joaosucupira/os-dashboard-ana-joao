import ctypes
import os
import subprocess
import sys

# --- COMPILAÇÃO AUTOMÁTICA DO AJUDANTE C (VERSÃO ROBUSTA) ---

try:
    # Obtém o caminho absoluto para o diretório 'utils'
    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    # Define os caminhos absolutos para o código-fonte e para a biblioteca compilada
    c_helper_source = os.path.join(dir_path, 'helper.c')
    c_helper_lib = os.path.join(dir_path, 'helper.so')

    # Checa se a compilação é necessária
    compile_needed = not os.path.exists(c_helper_lib) or os.path.getmtime(c_helper_source) > os.path.getmtime(c_helper_lib)

    if compile_needed:
        print(f"INFO: Compilação do ajudante C necessária. Compilando '{c_helper_source}'...")
        
        # Garante que o compilador gcc está disponível
        if subprocess.call(['which', 'gcc'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print("ERRO CRÍTICO: Compilador 'gcc' não encontrado. Por favor, instale o gcc ('sudo apt-get install build-essential').", file=sys.stderr)
            sys.exit(1)

        # Comando de compilação
        compile_command = ['gcc', '-shared', '-o', c_helper_lib, '-fPIC', c_helper_source]
        
        # Executa a compilação
        subprocess.run(compile_command, check=True)
        print("INFO: Ajudante compilado com sucesso.")
    else:
        print("INFO: Compilação do ajudante C não é necessária (o arquivo .so já está atualizado).")

    # Verificação final: Garante que o arquivo .so existe antes de continuar
    if not os.path.exists(c_helper_lib):
        print(f"ERRO CRÍTICO: O arquivo da biblioteca '{c_helper_lib}' não foi encontrado mesmo após a tentativa de compilação.", file=sys.stderr)
        sys.exit(1)

except (subprocess.CalledProcessError, FileNotFoundError) as e:
    print(f"ERRO CRÍTICO: Falha no processo de compilação do helper.c.", file=sys.stderr)
    print(f"Erro detalhado: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"ERRO INESPERADO durante a configuração da biblioteca: {e}", file=sys.stderr)
    sys.exit(1)

# --- CARREGAMENTO DA BIBLIOTECA E DEFINIÇÃO DAS FUNÇÕES (sem alterações) ---

# O resto do arquivo permanece o mesmo, pois o problema estava na criação da biblioteca.
libc_helper = ctypes.CDLL(c_helper_lib)

class SimpleStat(ctypes.Structure):
    _fields_ = [
        ('size', ctypes.c_longlong), ('mtime', ctypes.c_long),
        ('is_dir', ctypes.c_int), ('mode', ctypes.c_int),
    ]

get_simple_stat = libc_helper.get_simple_stat
get_simple_stat.argtypes = [ctypes.c_char_p, ctypes.POINTER(SimpleStat)]
get_simple_stat.restype = ctypes.c_int

def get_file_info(path):
    stats = SimpleStat()
    path_bytes = path.encode('utf-8')
    if get_simple_stat(path_bytes, ctypes.byref(stats)) != 0:
        return None
    permissions = oct(stats.mode)[-3:]
    return {"size": stats.size, "is_dir": bool(stats.is_dir), "permissions": permissions, "mtime": stats.mtime}

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