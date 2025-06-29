# teste_semaforo_verboso.py
import sysv_ipc
import time
import os
import sys

# Tenta importar a biblioteca e falha de forma clara se não estiver instalada
try:
    import sysv_ipc
except ImportError:
    print("ERRO: A biblioteca 'sysv_ipc' não está instalada.")
    print("Por favor, execute: pip install sysv_ipc")
    sys.exit(1)

# Chave única para o semáforo.
KEY = 12345 

try:
    # Tenta criar um novo semáforo. Se já existir, vai dar erro.
    print(f"Tentando criar um semáforo com a chave {KEY}...")
    semaphore = sysv_ipc.Semaphore(KEY, sysv_ipc.IPC_CREX)
    print(">>> SUCESSO! Semáforo criado.")
    print(f"    ID do Processo (PID): {os.getpid()}")
    print(f"    ID do Semáforo (semid): {semaphore.id}")
    print("\n--- O semáforo está ATIVO. ---")
    print("Agora é o momento de verificar o arquivo /proc/sysvipc/sem e testar seu dashboard.")
    print("Pressione Ctrl+C para sair e remover o semáforo.")
    
    # Mantém o processo vivo
    while True:
        time.sleep(1)

except sysv_ipc.ExistentialError:
    print(f"\n>>> ERRO: O semáforo com a chave {KEY} já existe!")
    print("Execute 'sudo ipcrm -a' para limpar os semáforos antigos e tente novamente.")
    sys.exit(1)

except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
    sys.exit(1)

finally:
    # Garante que o semáforo seja removido ao sair com Ctrl+C
    # Usamos 'locals()' para verificar se a variável 'semaphore' foi criada
    if 'semaphore' in locals():
        print("\nSaindo... Removendo o semáforo.")
        semaphore.remove()
        print("Semáforo removido com sucesso.")