#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include "crypto-algorithms/sha256.h"


#define ROUND 16

const uint8_t IP[64] = {
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
};

const uint8_t FP[64] = {
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25
};

const uint8_t E[48] = {
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
};

const uint8_t P[32] = {
    16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25
};

const uint8_t PL[28] = {
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36
};

const uint8_t PR[28] = {
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
};

const uint8_t P2[48] = {
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
};

// Input
uint8_t A[64] = {0};

// Key
const uint8_t B[64] = {
    'Y', 'Y', 'Y', 'E', 'E', 'E', 'E', 'A',
    'Y', 'Y', 'Y', 'E', 'E', 'E', 'E', 'I',
    'Y', 'Y', 'Y', 'E', 'E', 'E', 'E', 'S',
    'Y', 'Y', 'Y', 'E', 'E', 'E', 'E', '3',
    'Y', 'Y', 'Y', 'Y', 'E', 'E', 'E', '{',
    'Y', 'Y', 'Y', 'Y', 'E', 'E', 'E', '_',
    'Y', 'Y', 'Y', 'Y', 'E', 'E', 'E', '_',
    'Y', 'Y', 'Y', 'Y', 'E', 'E', 'E', '}'
};

// Flag = AIS3{0Ur_5Up3r_53cUr3_DES_5ti11_h45_w34k_k3y_LOL}
const uint8_t C[64] = {
    0xd4, 0xcf, 0x20, 0x44, 0x81, 0x13, 0xcf, 0x54,
    0x6e, 0xd3, 0x50, 0xef, 0x53, 0xd9, 0xd9, 0x18,
    0xd3, 0xd1, 0x11, 0x64, 0xda, 0xb8, 0x6c, 0x25,
    0xfb, 0x08, 0x60, 0x52, 0xe9, 0x59, 0x5c, 0x52,
    0x6b, 0xea, 0x8f, 0x14, 0x44, 0xd9, 0xc8, 0xae,
    0x10, 0xc8, 0x9d, 0x7f, 0xcf, 0xc6, 0x3e, 0x3e,
    0x91, 0xaa, 0xa3, 0x21, 0xd6, 0x7b, 0x40, 0xe6,
    0x13, 0x4a, 0xba, 0x0a, 0x10, 0x23, 0x50, 0x28,
};

const uint8_t D[] = "AIS3{5TrIn95!?(._.||| )n0T_tHe_ca5e_t2y_hard3r}";

static inline void xor (uint8_t* a, uint8_t* b, size_t len) {
    for (int i=0; i<len; i++) {
        a[i] ^= b[i];
    }
}

int main () {
    fputs("[*] Welcome to the demo platform of our Secure DES.\n", stderr);
    fputs("[*] Everyone knows that DES is insecure, mainly due to its tiny keyspace.\n", stderr);
    fputs("[*] So we made a super strong 512 bits variant.\n", stderr);
    fputs("[*] Let's make DES great again!!!\n", stderr);
    fputs("\n", stderr);
    fputs("[>] Enter the flag\n", stderr);
    fputs(">>> ", stderr);
    fflush(stderr);
    memset(A, 0, 64);
    read(0, A, 64);
    fputs("\n", stderr);

    /*-- Initial Permutation --*/
    uint8_t A_ip[64];
    for (int i=0; i<64; i++) {
        A_ip[i] = A[IP[i] - 1];
    }
    memcpy(A, A_ip, 64);

    /*-- Key Schedule Initialization --*/
    uint8_t K[56];
    for (int i=0; i<28; i++) {
        K[i] = B[PL[i] - 1];
        K[i+28] = B[PR[i] - 1];
    }

    /*-- Feistel Network --*/
    for (int round=0; round<ROUND; round++) {
        /*-- Feistel Function --*/
        /*-- Expansion --*/
        uint8_t A_e[48];
        for (int i=0; i<48; i++) {
            A_e[i] = A[E[i] - 1 + 32];
        }

        /*-- Shift Key Schedule State --*/
        uint8_t l = K[0], r = K[28];
        for (int i=0; i<28; i++) {
            K[i] = K[i+1];
            K[i+28] = K[i+1+28];
        }
        K[27] = l;
        K[55] = r;

        /*-- Key Mixing --*/
        for (int i=0; i<48; i++) {
            A_e[i] ^= K[P2[i] - 1];
        }

        /*-- Substitution by SHA256 --*/
        uint8_t A_s[SHA256_BLOCK_SIZE];
        SHA256_CTX ctx;
        sha256_init(&ctx);
        sha256_update(&ctx, A_e, 48);
        sha256_final(&ctx, A_s);

        /*-- Permutation --*/
        uint8_t A_p[32];
        for (int i=0; i<32; i++) {
            A_p[i] = A_s[P[i] - 1];
        }

        /*-- Feistel Network --*/
        //                             |   | 
        xor(A, A_p, 32); //            +-F-| 
        if (round != ROUND - 1) { //   |   | 
            xor(A, A + 32, 32);//      '\ /'
            xor(A + 32, A, 32);//        X
            xor(A, A + 32, 32);//      ./ \.
        }//                            |   |
    }

    /*-- Final Permutation (e.g. Inverse of IP) --*/
    uint8_t A_fp[64];
    for (int i=0; i<64; i++) {
        A_fp[i] = A[FP[i] - 1];
    }
    memcpy(A, A_fp, 64);

    /*-- Output --*/
    fputs("[*] Result\n", stderr);
    for (int i=0; i<64; i+=8) {
        fputs("[=] ", stderr);
        for (int j=i; j<i+8; j++) {
            fprintf(stderr, "0x%02x, ", A[j]);
        }
        fputs("\n", stderr);
    }
    fputs("\n", stderr);

    // fputs("[*] Result - Bin\n", stderr);
    // fputs("[=] ", stderr);
    // fwrite(A, 1, 64, stdout);
    // fflush(stdout);
    // fputs("\n", stderr);
    // fputs("\n", stderr);

    /*-- Show result --*/
    if (memcmp(A, C, 64) == 0) {
        fputs("[+] Correct\n", stderr);
    } else {
        fputs("[+] Wrong\n", stderr);
    }
}
