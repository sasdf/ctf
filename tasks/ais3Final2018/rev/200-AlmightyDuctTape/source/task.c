#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/*-- sha256 constants, but it is not sha256 xDDD --*/
#define N (256 / 8)
#define ROUND 64
uint32_t keys[] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

unsigned char flag[N] = {0};

// Flag = AIS3{DuctT4p3_f1X3s_3ve2ytH1n9}\n
unsigned char target[N] = {
    0x53, 0x6c, 0x08, 0x87, 0xcb, 0x1d, 0xa2, 0x46,
    0x21, 0x7c, 0xf5, 0xcb, 0x03, 0x54, 0x7e, 0x25,
    0x0b, 0xae, 0x29, 0xdb, 0x88, 0x79, 0x0c, 0x3c,
    0x99, 0x0e, 0x48, 0x6c, 0xdc, 0xda, 0xc8, 0x2b,
};

/*-- SBox from AES --*/
unsigned char sbox[256] =  {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};


/*-- TEA code from wikipedia, delta constant is modified --*/
void encrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0, i;           /* set up */
    uint32_t delta = k[4];                         /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i < 32; i++) {                       /* basic cycle start */
        sum += delta;
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

/*-- Perform byte substitution using SBox from AES --*/
void substitute (void* buf, size_t len) {
    uint8_t* cbuf = (uint8_t*) buf;
    for (int i=0; i<len; i++) {
        cbuf[i] = sbox[cbuf[i]];
    }
}

int main () {
    /*-- Reading input --*/
    fputs("[>] Enter the flag\n", stderr);
    fputs(">>> ", stderr);
    fflush(stderr);
    read(0, flag, N);
    fputs("\n", stderr);


    /*-- Perturb the input --*/
    for (int i=0; i<N; i++) {
        flag[i] ^= i ^ keys[0];
        flag[i] = (flag[i] >> 3) | (flag[i] << (8 - 3));
    }

    uint32_t* u32flag = (uint32_t*) flag;
    uint32_t iv0 = keys[1], iv1 = keys[2];


    /*-- Encrypt multiple times for avalanche effect --*/
    for (int r=0; r<ROUND; r++) {
        /*-- TEA with CBC mode --*/
        for (int i=0; i<N/4; i+=2) {
            u32flag[i]   ^= iv0;
            u32flag[i+1] ^= iv1;
            encrypt(&u32flag[i], &keys[3]);
            substitute(&u32flag[i], 8);
            iv0 = u32flag[i];
            iv1 = u32flag[i+1];
        }
    }


    /*-- DEBUG --*/
    fputs("[*] Result\n", stderr);
    for (int i=0; i<N; i+=8) {
        fputs("[=] ", stderr);
        for (int j=i; j<N && j<i+8; j++) {
            fprintf(stderr, "0x%02x, ", flag[j]);
        }
        fputs("\n", stderr);
    }
    fputs("\n", stderr);


    /*-- Check the result --*/
    if (memcmp(flag, target, N) == 0) {
        fputs("[+] Correct\n", stderr);
    } else {
        fputs("[!] Wrong\n", stderr);
    }
}
