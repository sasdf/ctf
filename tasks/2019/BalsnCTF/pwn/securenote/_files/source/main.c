#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include "aes.h"

typedef union {
    uint64_t u64[2];
    uint8_t u8[16];
} Counter;

uint8_t key[16] = {0};
Counter* counter;

struct Note {
    char* content;
    Counter ctr;
};

#define MAX_NOTES 4
struct Note notes[MAX_NOTES];

void aes_ctr_next_block (Counter* ctr, uint8_t* out) {
    ctr->u64[0] = ctr->u64[0] * 3133731337 + 0x1337;
    ctr->u64[1] = 0x1337;
    struct AES_ctx aes;
    AES_init_ctx(&aes, key);
    memcpy(out, ctr->u8, 16);
    AES_ECB_encrypt(&aes, out);
}
    
   
void aes_ctr_new_nonce (Counter* ctr) {
    ctr->u64[0] = ctr->u64[0] * 0xdeadbeef + 0xcafe;
    ctr->u64[1] = 0x1337;
}
    
   
void aes_ctr_encrypt (Counter* ctr, char *buf) {
    uint8_t keystream[16];
    aes_ctr_next_block(ctr, keystream);
    char c;
    int i = 0;
    do {
        if (i == 16) {
            aes_ctr_next_block(ctr, keystream);
            i = 0;
        }
        c = *buf;
        *(buf++) = c ^ keystream[i++];
    } while (c);
}
    
void aes_ctr_decrypt (Counter* ctr, char *buf) {
    uint8_t keystream[16];
    aes_ctr_next_block(ctr, keystream);
    char c;
    int i = 0;
    do {
        if (i == 16) {
            aes_ctr_next_block(ctr, keystream);
            i = 0;
        }
        *buf ^= keystream[i++];
    } while (*(buf++));
}

uint32_t read_idx(uint32_t max) {
    char buf[11];
    printf("idx [0 ~ %d]: ", max - 1);
    memset(buf, 0, sizeof(buf));
    int nbyte = read(0, buf, sizeof(buf) - 1);
    if (nbyte <= 0) exit(0);
    uint32_t idx = strtoul(buf, NULL, 0);
    if (idx >= max) {
        puts("Invalid number :<");
        exit(0);
    }
    return idx;
}

void create_note() {
    puts("Where to place the note?");
    uint32_t idx = read_idx(MAX_NOTES);
    if (notes[idx].content != NULL) {
        puts("Not empty :<");
        exit(0);
    }
    
    char buf[1000];
    memset(buf, 0, sizeof(buf));
    puts("Content:");
    int nbyte = read(0, buf, sizeof(buf) - 1);
    if (nbyte <= 0) exit(0);
    
    if (buf[nbyte - 1] == '\n') {
        buf[nbyte - 1] = 0;
    }

    char* note = malloc(nbyte);

    aes_ctr_new_nonce(counter);
    memcpy(&notes[idx].ctr, counter, sizeof(Counter));
    strcpy(note, buf);
    aes_ctr_encrypt(counter, note);
    notes[idx].content = note;
}
    
void show_note () {
    puts("Where is the note?");
    uint32_t idx = read_idx(MAX_NOTES);
    if (notes[idx].content == NULL) {
        puts("Empty :<");
        exit(0);
    }
    Counter ctr;
    memcpy(&ctr, &notes[idx].ctr, sizeof(Counter));
    char* note = notes[idx].content;
    aes_ctr_decrypt(&ctr, note);
    puts(note);
    memcpy(&ctr, &notes[idx].ctr, sizeof(Counter));
    aes_ctr_encrypt(&ctr, note);
}

void delete_note () {
    puts("Where is the note?");
    uint32_t idx = read_idx(MAX_NOTES);
    if (notes[idx].content == NULL) {
        puts("Empty :<");
        exit(0);
    }
    free(notes[idx].content);
    memset(&notes[idx], 0, sizeof(struct Note));
}

void init() {
    alarm(777);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    counter = malloc(sizeof(Counter));
    memset(counter, 0, sizeof(Counter));
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0) exit(-1);
    int res = read(fd, key, 16);
    if (res != 16) exit(-1);
    res = read(fd, counter->u8, 8);
    if (res != 8) exit(-1);
    counter->u64[1] = 0x1337;
    close(fd);
}

void menu () {
    puts(".-----------------------.");
    puts("| 0 - Create a new note |");
    puts("| 1 - Show a note       |");
    puts("| 2 - Delete a note     |");
    puts("| 3 - Exit              |");
    puts("'-----------------------'");
}
    
int main (int argc, char* argv[]) {
    init();
    for (int i=0; i<1337; i++) {
        menu();
        uint32_t cmd = read_idx(4);
        switch (cmd) {
            case 0:
                create_note();
                break;
            case 1:
                show_note();
                break;
            case 2:
                delete_note();
                break;
            case 3:
                exit(0);
                break;
        }
    }
}
