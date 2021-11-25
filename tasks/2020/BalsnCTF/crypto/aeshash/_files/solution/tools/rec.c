#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <fcntl.h>
#include <unistd.h>
#include <wmmintrin.h>
#include <tmmintrin.h>
#include "aes.c"


#define unlikely(x) __builtin_expect(!!(x), 0)
#define likely(x) __builtin_expect(!!(x), 1)

void SetState(state_t* state, const uint8_t* value) {
    uint8_t i,j;
    for (i = 0; i < 4; ++i)
        for (j = 0; j < 4; ++j)
            (*state)[i][j] = value[(i * 4) + j];
}

void GetState(const state_t* state, uint8_t* value) {
    uint8_t i,j;
    for (i = 0; i < 4; ++i)
        for (j = 0; j < 4; ++j)
            value[(i * 4) + j] = (*state)[i][j];
}

void XorState(state_t* dest, const state_t* state) {
    uint8_t i,j;
    for (i = 0; i < 4; ++i)
        for (j = 0; j < 4; ++j)
            (*dest)[i][j] ^= (*state)[i][j];
}

void printmat(const uint8_t* val) {
    for (int i=0; i<4; i++) {
        for (int j=0; j<4; j++) {
            fprintf(stderr, "0x%02x, ", val[i * 4 + j]);
        }
        fprintf(stderr, "\n");
    }
    fprintf(stderr, "\n");
}

void MixSingleColumn(uint8_t* arr) {
    uint8_t val[16];
    memcpy(val, arr, 4);
    state_t state;
    SetState(&state, val);
    MixColumns(&state);
    GetState(&state, val);
    memcpy(arr, val, 4);
}

void InvMixSingleColumn(uint8_t* arr) {
    uint8_t val[16];
    memcpy(val, arr, 4);
    state_t state;
    SetState(&state, val);
    InvMixColumns(&state);
    GetState(&state, val);
    memcpy(arr, val, 4);
}

void PrintState(const state_t* state) {
    uint8_t val[16];
    GetState(state, val);
    printmat(val);
}

void SingleRound(state_t* state) {
    uint8_t round_key[16];
    GetState(state, round_key);
    ShiftRows(state);
    SubBytes(state);
    MixColumns(state);
    AddRoundKey(0, state, round_key);
}

void SubMixDiff(uint8_t v, uint8_t d, uint8_t x, uint8_t out[]) {
    uint8_t ap = sbox[v] ^ sbox[v^d];
    uint8_t apm[4] = {0, 0, 0, 0};
    apm[x] = ap;
    MixSingleColumn(apm);
    memcpy(out, apm, 4);
}

int Check3Round(uint8_t states[][4], int N, uint8_t va, uint8_t ve, uint8_t x, uint8_t y, uint8_t z) {
    // Initialize possible values
    uint8_t vep0s[256];
    int num_vep0s = 256;
    for (int i=0; i<256; i++) vep0s[i] = i;

    for (int a=1; a<N; a++) {
        uint8_t apm[5];
        SubMixDiff(va, a, 0, apm);
        apm[0] ^= a;
        apm[4] = 0;
        uint8_t e = apm[x];

        uint8_t epm[4];
        SubMixDiff(ve, e, x, epm);
        // fprintf(stderr, "epm: %02x %02x %02x %02x\n", epm[0], epm[1], epm[2], epm[3]);
        uint8_t g = apm[y] ^ epm[z];

        uint8_t num_nxt_vep0s = 0;
        for (int i=0; i<num_vep0s; i++) {
            uint8_t vep0 = vep0s[i];
            uint8_t ep0p = sbox[vep0] ^ sbox[vep0 ^ g];
            if (ep0p == states[a][z]) {
                vep0s[num_nxt_vep0s++] = vep0;
            }
        }
        num_vep0s = num_nxt_vep0s;
        // fprintf(stderr, "num_vep0s: %d %d\n", a, num_vep0s);
        if (num_vep0s == 0) break;
    }
    return num_vep0s;
}

void reconstruct(const int params[], uint64_t final_states[], int N, uint8_t *out_va, uint8_t out[]) {
    int col = params[0], aux = params[1];
    params += 2;

    uint8_t states[256][4];
    uint32_t state0 = final_states[0] >> (col * 32);
    for (int a=1; a<N; a++) {
        *(uint32_t*)&states[a] = (final_states[a] >> (col * 32)) ^ state0;
        InvMixSingleColumn(states[a]);
    }

    int va, vb, vc, vd, ve, vf, num;

    for (va=0; va<256; va++) {
        for (ve=0; ve<256; ve++) {
            num = Check3Round(states, N, va, ve, params[0], params[1], params[2]);
            if (num) {
                fprintf(stderr, "Found: va=%02x\n", va);
                fprintf(stderr, "Found: v[%d]=%02x, num=%d\n", params[0], ve, num);
                break;
            }
        }
        if (num) break;
    }
    assert(num > 0);

    *out_va = va;
    out[params[0]] = ve;

    for (int a=1; a<N; a++) {
        uint8_t apm[4];
        SubMixDiff(va, a, 0, apm);
        apm[0] ^= a;

        uint8_t ep = sbox[ve] ^ sbox[ve ^ apm[aux]];
        states[a][aux] ^= ep;
    }

    for (int z=0; z<3; z++) {
        params += 3;
        for (ve=0; ve<256; ve++) {
            num = Check3Round(states, N, va, ve, params[0], params[1], params[2]);
            if (num) {
                fprintf(stderr, "Found: v[%d]=%02x, num=%d\n", params[0], ve, num);
                break;
            }
        }
        assert(num > 0);
        out[params[0]] = ve;
    }
}

int main () {
    int ret;
    uint8_t init_state[16] = {
        0xef, 0xbe, 0xad, 0xde,
        0, 0, 0, 0,
        0x10, 0x00, 0x10, 0x00, 
        0x10, 0x00, 0x10, 0x00, 
    };

    const int params[4][14] = {
        // col0 using next col
        { 1, 3, 3, 4, 0, 2, 4, 1, 1, 4, 2, 0, 3, 3 },
        // col1 using prev col
        { 0, 1, 1, 4, 0, 0, 1, 1, 3, 4, 2, 2, 4, 3 },
        // col2 using prev col
        { 1, 1, 1, 4, 0, 0, 1, 1, 3, 4, 2, 2, 4, 3 },
        // col3 using next col
        { 0, 3, 3, 4, 0, 2, 4, 1, 1, 4, 2, 0, 3, 3 },
    };


    uint8_t first_row[4];
    state_t ans;

    int N = 7;
    uint64_t input[25];
    ret = read(0, (uint8_t*)input, 25*8);
    assert (ret == 25*8);

    uint64_t final_states[4][256];
    for (int i=0; i<4; i++) {
        final_states[i][0] = input[0];
    }
    for (int i=0; i<4; i++) {
        for (int j=0; j<N-1; j++) {
            final_states[i][j+1] = input[i*(N-1)+j+1];
        }
    }

    for (int i=0; i<4; i++) {
        fprintf(stderr, "Col%d:\n", i);
        reconstruct(params[i], final_states[i], N, &first_row[i], ans[i]);
    }

    fprintf(stderr, "first: %02x %02x %02x %02x\n", first_row[0], first_row[1], first_row[2], first_row[3]);
    PrintState(&ans);

    ret = write(1, first_row, 4);
    assert (ret == 4);
    ret = write(1, ans, 16);
    assert (ret == 16);
}
