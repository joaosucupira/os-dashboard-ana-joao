# GerenciadorDisco.py (versão corrigida e robusta)

import os
import logging
import stat  # Importar o módulo 'stat' do Python
from utils.util_filesystem import get_fs_usage # Usaremos apenas a função de uso de disco
from utils.util_diretorio import GerenciadorDiretorio

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - [%(module)s] - %(message)s',
    handlers=[
        logging.FileHandler("dashboard_debug.log", mode='w'),
        logging.StreamHandler()
    ]
)

class GerenciadorDisco:

    def get_partitions_info(self):
        partitions = []
        try:
            with open("/proc/mounts", "r") as f:
                for line in f:
                    try:
                        parts = line.split()
                        if len(parts) < 3: continue
                        
                        mount_point = parts[1]
                        fs_type = parts[2]
                        
                        if fs_type in ["ext4", "vfat", "ntfs", "btrfs", "xfs"]:
                            if not os.path.isdir(mount_point):
                                continue
                            
                            usage = get_fs_usage(mount_point)
                            if usage:
                                partitions.append({ "device": parts[0], "mount_point": mount_point, "fs_type": fs_type, **usage })
                    except Exception:
                        continue
        except Exception as e:
            logging.error(f"Falha crítica ao ler /proc/mounts: {e}", exc_info=True)
            return []
        
        return partitions

    def list_directory_contents(self, path):
        contents = []
        if not os.path.isdir(path):
            return contents

        try:
            # Usamos o GerenciadorDiretorio para listar os nomes de forma eficiente
            with GerenciadorDiretorio(path) as gd:
                for entry in gd:
                    if entry.name in [".", ".."]:
                        continue
                    
                    full_path = os.path.join(path, entry.name)
                    
                    try:
                        # --- NOVA LÓGICA COM OS.STAT() ---
                        # Em vez de chamar get_file_info, usamos os.stat() que é mais confiável.
                        file_stats = os.stat(full_path)
                        
                        # Extrai as permissões do modo stat
                        permissions = stat.S_IMODE(file_stats.st_mode)
                        
                        info = {
                            "name": entry.name,
                            "path": full_path,
                            "size": file_stats.st_size,
                            "is_dir": stat.S_ISDIR(file_stats.st_mode),
                            "permissions": f"{permissions:o}", # Formata como octal
                            "mtime": file_stats.st_mtime,
                        }
                        contents.append(info)

                    except (PermissionError, FileNotFoundError) as e:
                        # Se os.stat() falhar, registramos o erro e continuamos.
                        logging.warning(f"Ignorando arquivo inacessível '{full_path}'. Erro: {e}")
                        continue

        except PermissionError:
            logging.error(f"Permissão negada para acessar o diretório: {path}")
        except Exception as e:
            logging.critical(f"Erro não esperado ao listar o diretório '{path}': {e}", exc_info=True)

        # Ordena: diretórios primeiro, depois arquivos, ambos alfabeticamente
        contents.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        return contents