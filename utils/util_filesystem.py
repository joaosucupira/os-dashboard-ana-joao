import ctypes
import platform
import errno  
import sys   

# As definições das estruturas e a detecção de arquitetura 
class struct_statvfs(ctypes.Structure):
    _fields_ = [
        ('f_bsize', ctypes.c_ulong), ('f_frsize', ctypes.c_ulong),
        ('f_blocks', ctypes.c_ulonglong), ('f_bfree', ctypes.c_ulonglong),
        ('f_bavail', ctypes.c_ulonglong), ('f_files', ctypes.c_ulonglong),
        ('f_ffree', ctypes.c_ulonglong), ('f_favail', ctypes.c_ulonglong),
        ('f_fsid', ctypes.c_ulong), ('f_flag', ctypes.c_ulong),
        ('f_namemax', ctypes.c_ulong), ('__f_spare', ctypes.c_int * 6),
    ]

# Se for AMD
machine_arch = platform.machine()
if machine_arch == "x86_64":
    class struct_stat(ctypes.Structure):
        _fields_ = [
            ('st_dev', ctypes.c_uint64), ('st_ino', ctypes.c_uint64),
            ('st_nlink', ctypes.c_uint64), ('st_mode', ctypes.c_uint32),
            ('st_uid', ctypes.c_uint32), ('st_gid', ctypes.c_uint32),
            ('__pad0', ctypes.c_int32), ('st_rdev', ctypes.c_uint64),
            ('st_size', ctypes.c_int64), ('st_blksize', ctypes.c_int64),
            ('st_blocks', ctypes.c_int64), ('st_atime', ctypes.c_int64),
            ('st_atime_ns', ctypes.c_int64), ('st_mtime', ctypes.c_int64),
            ('st_mtime_ns', ctypes.c_int64), ('st_ctime', ctypes.c_int64),
            ('st_ctime_ns', ctypes.c_int64), ('__unused', ctypes.c_int64 * 3),
        ]
else: # Se for ARM
    class struct_stat(ctypes.Structure):
        _fields_ = [
            ('st_dev', ctypes.c_ulong), ('st_ino', ctypes.c_ulong),
            ('st_mode', ctypes.c_uint), ('st_nlink', ctypes.c_uint),
            ('st_uid', ctypes.c_uint), ('st_gid', ctypes.c_uint),
            ('st_rdev', ctypes.c_ulong), ('__pad1', ctypes.c_ulong),
            ('st_size', ctypes.c_long), ('st_blksize', ctypes.c_int),
            ('__pad2', ctypes.c_int), ('st_blocks', ctypes.c_long),
            ('st_atime', ctypes.c_long), ('st_atime_ns', ctypes.c_ulong),
            ('st_mtime', ctypes.c_long), ('st_mtime_ns', ctypes.c_ulong),
            ('st_ctime', ctypes.c_long), ('st_ctime_ns', ctypes.c_ulong),
            ('__unused4', ctypes.c_uint), ('__unused5', ctypes.c_uint),
        ]
# Definição das chamadas de sistema necessárias

libc = ctypes.CDLL(None, use_errno=True)
statvfs = libc.statvfs
statvfs.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_statvfs)]
statvfs.restype = ctypes.c_int

xstat = libc.__xstat
xstat.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(struct_stat)]
xstat.restype = ctypes.c_int

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
    return {"total": total_gb, "used": used_gb, "free": free_gb, "use_perc": use_perc}

def get_file_info(path):
    file_stats = struct_stat()
    path_bytes = path.encode('utf-8')
    
    if xstat(1, path_bytes, ctypes.byref(file_stats)) != 0:

        # Se a chamada falhar, capturamos o código de erro (errno)
        error_code = ctypes.get_errno()
        # Traduzimos o código para uma mensagem legível (ex: 'EPERM', 'EACCES')
        error_message = errno.errorcode.get(error_code, f"Código de erro desconhecido {error_code}")
        
        # Imprimimos uma mensagem de depuração detalhada na saída de erro padrão
        print(
            f"DEBUG: A chamada xstat falhou para o caminho '{path}' "
            f"com errno {error_code} ({error_message})",
            file=sys.stderr
        )

        return None

    is_dir = (file_stats.st_mode & S_IFDIR) != 0
    return {"size": file_stats.st_size, "is_dir": is_dir, "permissions": oct(file_stats.st_mode)[-3:], "mtime": file_stats.st_mtime}