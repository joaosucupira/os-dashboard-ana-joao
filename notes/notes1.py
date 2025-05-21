
# Joao: Essa biblioteca traz a biblioteca padrão C pra manipula processos linux e
# precisa de conhecimento da tabelas de syscalls para ser usada propriamente.
import ctypes

# Joao: variável com o objeto que chama as bibliotecas C
libc = ctypes.CDLL(None)

# Joao: configuração do tipo de retorno
libc.getpid.restype = ctypes.c_int

# Joao: variável recebendo process id do proceso atual
pid = libc.getpid()

msg = b'syscall do write\n'
msg2 = f'syscall do getpid atual = {pid}\n'.encode()

libc.write.restype = ctypes.c_ssize_t

libc.write(1, msg, len(msg))
libc.write(1, msg2, len(msg2))