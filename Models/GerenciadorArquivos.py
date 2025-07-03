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
                            pipes = 0
                            outros = 0
                            
                            # Percorre todos os descritores de arquivos do processo
                            # e conta os arquivos, sockets e mutexes
                            try:
                                for fd_entry in fd_gd:
                                    if fd_entry.is_symlink():
                                        try:
                                            target = fd_entry.readlink()
                                            # Conta quantidade de sockets
                                            if target.startswith("socket:"):
                                                sockets += 1
                                            # Conta quantidade de pipes
                                            elif target.startswith("pipe:"):
                                                pipes += 1
                                            # Conta quantidade de arquivos abertos
                                            elif target.startswith("/"):
                                                arquivos += 1
                                            # Conta outros tipos de arquivos
                                            elif target.startswith("anon_inode:"):
                                                outros += 1
                                        except Exception:
                                            continue

                            except Exception:
                                pass


                        # Caminho para acessar o nome e estado do processo
                        try:
                            with open(status_path) as f:

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
                                "pipes": pipes,
                                "outros": outros

                            })
                        except Exception:
                            pass
                    except Exception:
                        pass

        processos.sort(key=lambda p: (p['arquivos'], p['sockets'], p['pipes']), reverse=True)
        return processos