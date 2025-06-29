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
                            mutexes = 0
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
                                            # Conta quantidade de mutexes nomeados (sugestao do gemini)
                                            elif target.startswith("/dev/shm/sem."):
                                                mutexes += 1
                                            # Conta quantidade de mutexes anonimos (sugestao do copilot)
                                            elif "anon_inode:mutex" in target:
                                                mutexes += 1
                                            # Conta quantidade de arquivos abertos
                                            elif target.startswith("/"):
                                                arquivos += 1
                                            elif target.startswith("anon_inode:"):
                                                outros += 1
                                        except Exception:
                                            continue

                            except Exception:
                                pass

                            # conta quantidade de futexes (acho que esse arquivo só existe no kernel >= 5.4) (susgestao do gemini)
                            futex_path = f"/proc/{pid}/futexes"
                            try:
                                with open(futex_path, "r") as f:
                                    # Cada linha corresponde a um futex em espera
                                    mutexes += len(f.readlines())
                            except PermissionError as e:
                                # print(f"Não foi possível acessar {futex_path} para o processo {pid}: {e}")
                                pass
                            except FileNotFoundError:
                                pass

                            # Conta a quantidade de mutexes sysv (sugestao do gemini)
                            try:
                                with open("/proc/sysvipc/sem", "r") as f:
                                    # Pula a linha de cabeçalho
                                    next(f)
                                    
                                    for linha in f:
                                        partes = linha.split()
                                        # Colunas de interesse: key, semid, owner, perms, nsems, cpid, lpid
                                        if len(partes) >= 7:
                                            try:
                                                cpid = int(partes[5])
                                                lpid = int(partes[6])
                                                
                                                if int(pid) == cpid or int(pid) == lpid:
                                                    mutexes += 1
                                            except (ValueError, IndexError):
                                                continue
                            except FileNotFoundError as e:
                                # O arquivo pode não existir se o módulo de kernel não estiver carregado
                                # print(f"Arquivo sysvipc/sem não encontrado para o processo {pid}: {e}")
                                pass
                            except Exception as e:
                                # Outros erros (ex: permissão)
                                # print(f"Erro ao acessar sysvipc/sem para o processo {pid}: {e}")
                                pass

                            # Conta a quantidade de mutexes (forma como esta no repo suhbrasil)
                            try:
                                with open(status_path, 'r') as status_file:
                                    for line in status_file:
                                        # print("checking line:", line)
                                        if 'semaphores' in line.lower() or 'mutex' in line.lower():
                                            mutexes += 1
                            except Exception as e:
                                # logging.error(f"Erro ao ler status do processo {pid}: {e}")
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
                                "pipes": pipes,
                                "mutexes": mutexes,
                                "outros": outros

                            })
                        except Exception:
                            pass
                    except Exception:
                        pass

        processos.sort(key=lambda p: (p['arquivos'], p['sockets'], p['pipes'], p['mutexes']), reverse=True)
        return processos