# funções de baixo nível para pegar informações de arquivos e partições, usando chamadas diretas da biblioteca C (libc).

import ctypes
# O import 'stat' foi removido pois não será mais utilizado.

# Mapeamento das estruturas de dados que o C usa.

# 'struct stat': informações de um arquivo (tamanho, permissões, etc).
class struct_stat(ctypes.Structure):
    _fields_ = [
        ('st_dev', ctypes.c_uint64),      # ID do dispositivo
        ('st_ino', ctypes.c_uint64),      # Inode
        ('st_nlink', ctypes.c_uint64),    # Número de links
        ('st_mode', ctypes.c_uint32),     # Permissões
        ('st_uid', ctypes.c_uint32),      # User ID
        ('st_gid', ctypes.c_uint32),      # Group ID
        ('__pad0', ctypes.c_int32),       # Padding para alinhamento
        ('st_rdev', ctypes.c_uint64),     # ID do dispositivo (se especial)
        ('st_size', ctypes.c_int64),      # Tamanho em bytes
        ('st_blksize', ctypes.c_int64),   # Tamanho do bloco para I/O
        ('st_blocks', ctypes.c_int64),    # Número de blocos de 512B alocados
        ('st_atime', ctypes.c_int64),     # Último acesso (timestamp)
        ('st_atime_ns', ctypes.c_int64),  # Nanossegundos
        ('st_mtime', ctypes.c_int64),     # Última modificação (timestamp)
        ('st_mtime_ns', ctypes.c_int64),  # Nanossegundos
        ('st_ctime', ctypes.c_int64),     # Última mudança (timestamp)
        ('st_ctime_ns', ctypes.c_int64),  # Nanossegundos
        ('__unused', ctypes.c_int64 * 3), # Reservado
    ]

# 'struct statvfs': informações sobre uma partição (espaço total, livre, etc).
class struct_statvfs(ctypes.Structure):
    _fields_ = [
        ('f_bsize', ctypes.c_ulong),
        ('f_frsize', ctypes.c_ulong),
        ('f_blocks', ctypes.c_ulonglong), # ulonglong para garantir 64 bits
        ('f_bfree', ctypes.c_ulonglong),
        ('f_bavail', ctypes.c_ulonglong),
        ('f_files', ctypes.c_ulonglong),
        ('f_ffree', ctypes.c_ulonglong),
        ('f_favail', ctypes.c_ulonglong),
        ('f_fsid', ctypes.c_ulong),
        ('f_flag', ctypes.c_ulong),
        ('f_namemax', ctypes.c_ulong),
        ('__f_spare', ctypes.c_int * 6),
    ]

libc = ctypes.CDLL(None)

# Prepara a função 'statvfs' para ser chamada
statvfs = libc.statvfs
statvfs.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_statvfs)]
statvfs.restype = ctypes.c_int

# Prepara a função 'stat', a versão padrão e mais segura
stat_func = libc.stat
stat_func.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_stat)]
stat_func.restype = ctypes.c_int

# Constante para checar se um arquivo é um diretório
S_IFDIR = 0o040000

def get_fs_usage(path):
    fs_stats = struct_statvfs()
    path_bytes = path.encode('utf-8')
    if statvfs(path_bytes, ctypes.byref(fs_stats)) != 0:
        return None

    total_gb = (fs_stats.f_blocks * fs_stats.f_frsize) / (1024**3)
    free_gb = (fs_stats.f_bfree * fs_stats.f_frsize) / (1024**3)
    used_gb = total_gb - free_gb
    use_perc = (used_gb / total_gb) * 100 if total_gb > 0 else 0

    return { "total": total_gb, "used": used_gb, "free": free_gb, "use_perc": use_perc }

# A função 'get_file_info' foi corrigida e unificada.
def get_file_info(path):
    file_stats = struct_stat()
    path_bytes = path.encode('utf-8')
    
    if stat_func(path_bytes, ctypes.byref(file_stats)) != 0:
        return None

    is_dir = (file_stats.st_mode & S_IFDIR) != 0
    
    # --- CORREÇÃO APLICADA AQUI ---
    # Usamos uma máscara de bits para pegar apenas a parte das permissões do 'st_mode'
    # 0o777 é a máscara para permissões de usuário, grupo e outros (rwx rwx rwx)
    permissions = file_stats.st_mode & 0o777
    
    return {
        "size": file_stats.st_size,
        "is_dir": is_dir,
        # Formata o inteiro das permissões como uma string octal (ex: 755)
        "permissions": f"{permissions:o}",
        "mtime": file_stats.st_mtime,
    }