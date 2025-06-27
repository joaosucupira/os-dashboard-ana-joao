# Model especializado nas informações de arquivos e dispositivos de entrada e saida dos processos do sistema 
from utils.util_diretorio import GerenciadorDiretorio, uid_para_nome, state_id_para_nome

import logging

class GerenciadorArquivos:

    def listar_processos_e_arquivos(self):
        processos = []

        with GerenciadorDiretorio("/proc") as gd:
            for entry in gd:
                if entry.name.isdigit():
                    pid = entry.name
                    usuario = "N/A"
                    nome = "N/A"
                    uid = None

                    # Caminho para acessar o diretório de arquivos do processo
                    fd_path = f"/proc/{pid}/fd"
                    status_path = f"/proc/{pid}/status"

                    try:
                        # Um subgerenciador para lidar com o diretório de descritores de arquivos do processo
                        with GerenciadorDiretorio(fd_path) as fd_gd:
                            arquivos = 0
                            sockets = 0
                            mutexes = 0
                            
                            # Percorre todos os descritores de arquivos do processo
                            # e conta os arquivos, sockets e mutexes
                            try:
                                for fd_entry in fd_gd:
                                    if fd_entry.is_symlink():
                                        try:
                                            target = fd_entry.readlink()
                                            if target.startswith("socket:"):
                                                sockets += 1
                                            # elif "anon_inode:mutex" in target:
                                            #     mutexes += 1
                                            elif target.startswith("/"):
                                                arquivos += 1
                                            else:
                                                try:
                                                     with open(status_path, 'r') as status_file:
                                                        for line in status_file:
                                                            print("checking line:", line)
                                                            if 'semaphores' in line.lower() or 'mutex' in line.lower():
                                                                mutexes += 1
                                                except Exception as e:
                                                    logging.error(f"Erro ao ler status do processo {pid}: {e}")
                                                    continue
                                        except Exception:
                                            continue

                            except Exception:
                                pass

                        # Caminho para acessar o nome e estado do processo
                        try:
                            with open(f"/proc/{pid}/status") as f:

                                for line in f:
                                    if line.startswith("Name:"):
                                        nome = line.split()[1]
                                    elif line.startswith("Uid:"):
                                        uid = line.split()[1]
                            if uid is not None:
                                usuario = uid_para_nome(uid)

                            # Para cada processo, um dicionario com as informações coletadas
                            processos.append({
                                "pid": pid,
                                "nome": nome,
                                "usuario": usuario,
                                "arquivos": arquivos,
                                "sockets": sockets,
                                "mutexes": mutexes
                            })
                        except Exception:
                            continue
                    except Exception:
                        continue

        processos.sort(key=lambda p: (p['arquivos'], p['sockets'], p['mutexes']), reverse=True)
        return processos