#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("[!] Missing shellcode file.\n");
        exit(-1);
    }
    int fd = open(argv[1], O_RDONLY);
    void* addr = mmap(0xdeadbeef, 0x2000, PROT_EXEC|PROT_READ|PROT_WRITE, MAP_PRIVATE, fd, 0);
    asm("int3;");
    ((void (*)(void))(addr))();
}
