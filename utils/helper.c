#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

// Definimos uma estrutura simples para retornar apenas os dados que nos interessam.
// Isso evita problemas de compatibilidade com a struct stat completa.
struct SimpleStat {
    long long size; // Tamanho do arquivo
    long mtime;     // Tempo da última modificação
    int is_dir;     // Flag: 1 se for diretório, 0 caso contrário
    int mode;       // Permissões do arquivo
};

// Esta é a função que nosso Python irá chamar.
// Ela recebe um caminho e um ponteiro para a nossa estrutura simples.
int get_simple_stat(const char *path, struct SimpleStat *result) {
    struct stat statbuf;

    // Esta é a chamada de sistema real.
    if (stat(path, &statbuf) != 0) {
        // Se a chamada falhar, retorna -1.
        return -1;
    }

    // Se a chamada for bem-sucedida, preenchemos nossa estrutura simples.
    result->size = statbuf.st_size;
    result->mtime = statbuf.st_mtime;
    result->mode = statbuf.st_mode;
    
    // Verificamos se é um diretório.
    if (S_ISDIR(statbuf.st_mode)) {
        result->is_dir = 1;
    } else {
        result->is_dir = 0;
    }

    return 0; // Retorna 0 em caso de sucesso.
}