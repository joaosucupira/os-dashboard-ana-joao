# THREADS

# 1- imports
import time
import ctypes
# 2- instancia da biblioteca padrão
libc = ctypes.CDLL(None)
# 3 - definição do tipo de função usada pela thread
# void* funcion(void* arg)
THREAD_FUNC = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p) #retorno e parametro


# 4 - definição dos comandos da função usada peal thread
# O decorador @THREAD_FUNC converte a função Python em uma função C válida para ser usada por pthread_create.
@THREAD_FUNC # Esse decorador precisa estar no topo de toda função que for ser usada por uma thread
def thread_function_A(arg):
    for i in range(5):
        print(f'Thread monitora dos processos {i} rodando')
        time.sleep(1)
    return None

@THREAD_FUNC
def thread_function_B(arg):
    for i in range(10):
        print(f'Thread monitora da RAM {i} rodando')
        time.sleep(1)
    return None

@THREAD_FUNC
def thread_funciont_C(arg):
    for i in range(7):
        print(f'Thread monitora da memória de armazenamento {i} rodando')
        time.sleep(1)
    return None
# 5 - cria variável pthread_t p cada uma que eu queira instanciar

thread_A = ctypes.c_ulong()
thread_B = ctypes.c_ulong()
thread_C = ctypes.c_long()


# 6 - cria threads e guarda os resultados da criação, se der erro a condicional a seguir vai levantar exceção
# 6.1 - thread A
# 6.2 - Thread B

result_A = libc.pthread_create(
    ctypes.byref(thread_A),
    None,
    thread_function_A,
    None
)
result_B = libc.pthread_create(
    ctypes.byref(thread_B),
    None,
    thread_function_B,
    None
)

# 6.3 - Thread C
result_C = libc.pthread_create(
    ctypes.byref(thread_C),
    None,
    thread_funciont_C,
    None
)

# 7 - Previne erros de carregamento de thread
if result_A != 0 or result_B != 0 or result_C != 0:
    raise OSError("Falha ao carrega thread")

print("threads criadas")

# - Espera a thread terminar (join) basicamente ele serve para bloquear a função que a chama (nesse caso a main)
#   até que ela termine sua execução. 
libc.pthread_join(thread_A, None)
libc.pthread_join(thread_B, None)
libc.pthread_join(thread_C, None)

print("finished")