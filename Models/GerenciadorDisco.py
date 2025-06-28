import os
import logging
from utils.util_filesystem import get_fs_usage, get_file_info
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
        # logging.info("Iniciando a busca por partições.")
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
        
        # logging.info("Busca por partições finalizada.")
        return partitions

    def list_directory_contents(self, path):
        contents = []
        if not os.path.isdir(path):
            return contents

        # logging.info(f"Listando conteúdo do diretório: {path}")
        try:
            with GerenciadorDiretorio(path) as gd:
                for entry in gd:
                    if entry.name in [".", ".."]:
                        continue
                    
                    full_path = os.path.join(path, entry.name)
                    
                    try:
                        # --- CAMADA DE SEGURANÇA ---
                        # Antes de usar nossa syscall, fazemos um teste com a função segura do Python.
                        # Se os.stat() falhar, nós pulamos o arquivo.
                        os.stat(full_path.encode('utf-8'))
                        
                        # Se o teste acima passou, agora podemos chamar nossa função com mais segurança.
                        info = get_file_info(full_path)
                        
                        if info:
                            contents.append({ "name": entry.name, "path": full_path, **info })
                        else:
                            logging.warning(f"Nossa syscall get_file_info() falhou para '{full_path}', embora os.stat() tenha funcionado.")

                    except Exception as e:
                        # Se os.stat() falhar, registramos o erro e continuamos.
                        logging.warning(f"Ignorando arquivo inacessível '{full_path}'. Erro: {e}")
                        continue

        except PermissionError:
            logging.error(f"Permissão negada para acessar o diretório: {path}")
        except Exception as e:
            logging.critical(f"Erro não esperado ao listar o diretório '{path}': {e}", exc_info=True)

        contents.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        return contents