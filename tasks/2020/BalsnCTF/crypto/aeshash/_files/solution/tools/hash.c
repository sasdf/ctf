#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <fcntl.h>
#include <unistd.h>
#include <wmmintrin.h>
#include <tmmintrin.h>


#define unlikely(x) __builtin_expect(!!(x), 0)
#define likely(x) __builtin_expect(!!(x), 1)


#pragma pack(1)
union p8_u32 {
    uint32_t u32;
    uint8_t p8[4];
};

#pragma pack(1)
struct cand_t {
    union p8_u32 column;
    union p8_u32 shifted;
};

struct cand_t cands[4][1<<24];
uint64_t ncands[4][1<<16];

// {shifted_idx, column_idx, shifted_order, column_order}
int key_idx[4][4][4] = {
    /*             0             1             2             3    */
    /* 0 */ {{          }, {1, 3, 8, 0}, {2, 2, 8, 0}, {3, 1, 8, 0},},
    /* 1 */ {{3, 1, 0, 8}, {          }, {1, 3, 8, 0}, {2, 2, 8, 0},},
    /* 2 */ {{2, 2, 0, 8}, {3, 1, 0, 8}, {          }, {1, 3, 8, 0},},
    /* 3 */ {{1, 3, 0, 8}, {2, 2, 0, 8}, {3, 1, 0, 8}, {          },},
};

// Align src to dst
inline uint16_t key (struct cand_t* x, int src, int dst){
    int *ki = key_idx[src][dst];
    return (((uint16_t)x->shifted.p8[ki[0]]) << ki[2]) | (((uint16_t)x->column.p8[ki[1]]) << ki[3]);
}

inline uint16_t primary_key (struct cand_t* x, int col){
    if (col == 0) return key(x, 0, 1);
    else return key(x, col, 0);
}

int64_t key_u24(struct cand_t* x) {
    return ((int64_t)key(x, 3, 0) << 8) | x->column.p8[2];
}

int compare_u24 (const void * _a, const void * _b) {
    int64_t a = key_u24((struct cand_t*)_a);
    int64_t b = key_u24((struct cand_t*)_b);
    return a - b;
}

uint8_t shf_val[4][16] = {
    { 0,  5, 10, 15,   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1},
    { 4,  9, 14,  3,   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1},
    { 8, 13,  2,  7,   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1},
    {12,  1,  6, 11,   -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1},
};

void gen_candidate(uint8_t* _target) {
    memset(ncands, 0, sizeof(ncands));
    uint32_t* target = (uint32_t*)_target;
    #pragma omp parallel for num_threads(24)
    for (uint64_t s=0; s<(1ULL<<32); s+=4) {
        // Parallel Inverse MixColumn for (s, s+1, s+2, s+3)
        __m128i vec_repeat = _mm_setr_epi32(s, s, s, s);
        __m128i vec_inc = _mm_setr_epi32(0, 1, 2, 3);
        __m128i vec_init = _mm_add_epi32(vec_repeat, vec_inc);
        __m128i vec_state = _mm_aesimc_si128(vec_init);
        __m128i vec_v0 = _mm_aesdeclast_si128(vec_state, vec_init);

        // Indexing
        __m128i vec_shf = _mm_setr_epi8(0, 4, 8, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1);
        __m128i vec_v0s = _mm_shuffle_epi8(vec_v0, vec_shf);
        uint32_t v0s = _mm_cvtsi128_si32(vec_v0s);

        for (uint8_t si=0; si<4; si++, v0s >>= 8) {
            for (int i=0; i<4; i++) {
                if (unlikely((uint8_t)v0s == (uint8_t)target[i])) {
                    struct cand_t cand;
                    cand.column.u32 = (s + si) ^ target[i];

                    // Undo XorRoundKey and InvShiftRows
                    __m128i vec_s0 = _mm_xor_si128(vec_v0, vec_init);
                    __m128i vec_shf = _mm_load_si128((__m128i*)shf_val[si]);
                    __m128i vec_s0i = _mm_shuffle_epi8(vec_s0, vec_shf);
                    cand.shifted.u32 = _mm_cvtsi128_si32(vec_s0i);

                    uint16_t k = primary_key(&cand, i);
                    uint64_t idx = __sync_fetch_and_add(&ncands[i][k], 1);
                    // assert(idx <= 256);
                    idx += k * 256;
                    cands[i][idx] = cand;
                }
            }
        }
    }

    // Sanity check
    for (int i=0; i<4; i++)
        for (int j=0; j<(1<<16); j++)
            assert(ncands[i][j] == 256);
}

size_t hash_inverse (uint8_t* target_state, uint8_t* output, size_t output_size) {
    size_t output_limit = output_size / 16;

    fprintf(stderr, "Generating candidates\n");
    gen_candidate(target_state);

    fprintf(stderr, "Sorting by secondary index\n");
    #pragma omp parallel for num_threads(24)
    for (uint64_t i=0; i<(1<<24); i+=256) {
        qsort(&cands[3][i], 256, sizeof(struct cand_t), compare_u24);
    }

    fprintf(stderr, "Generating column 3 index\n");
    int8_t *idx3 = (int8_t*) malloc(1<<24);
    #pragma omp parallel for num_threads(24)
    for (uint64_t i=0; i<(1<<24); i++) { idx3[i] = -128; }
    #pragma omp parallel for num_threads(24)
    for (int64_t b=0; b<(1<<24); b+=256) {
        for (int64_t i=b+255; i>=b; i--) {
            int64_t k = key_u24(&cands[3][i]);
            int32_t diff = i - k;
            idx3[k] = diff;
            assert(abs(diff) < 127);
        }
    }

    fprintf(stderr, "Extracting keys\n");
    #define VARNAME(x, y) k ## x ## y ## s
    #define extract(x, y) \
        uint16_t *VARNAME(x, y) = (uint16_t*) malloc((1<<24) * sizeof(uint16_t));\
        for (uint64_t i=0; i<(1<<24); i++) { VARNAME(x, y)[i] = key(&cands[x][i], x, y); }

    extract(0, 2);
    extract(1, 2);
    extract(2, 1);
    extract(0, 3);
    extract(1, 3);
    extract(2, 3);
    extract(3, 0);
    extract(3, 1);
    extract(3, 2);

    fprintf(stderr, "Searching\n");
    uint64_t count = 0;
    #pragma omp parallel for num_threads(24)
    for (uint64_t bucket=0; bucket<(1<<24); bucket+=256) {

        // Building hash table
        #define HASHBITS 13
        uint8_t map_value[(1<<HASHBITS)][16][2];
        uint8_t map_count[(1<<HASHBITS)];
        memset(map_count, 0, sizeof(map_count));
        for (uint64_t i=0; i<256; i++) {
            uint64_t b = bucket + i;
            uint16_t k12 = k12s[b];
            uint16_t k = k12 >> (16 - HASHBITS);
            uint8_t idx = map_count[k]++;
            assert(idx < 16);
            map_value[k][idx][0] = (uint8_t)k12;
            map_value[k][idx][1] = i;
        }

        // Searching in k01 table
        for (uint64_t a=bucket; a<bucket+256; a++) {
            // Searching in k21 table
            uint64_t c = (uint64_t)k02s[a] * 256;
            uint64_t cend = c + 256;
            for (; c<cend; c++) {
                uint16_t k21 = k21s[c];
                uint16_t k = k21 >> (16 - HASHBITS);
                uint8_t cnt = map_count[k];
                for (int i=0; i<cnt; i++) {
                    if (unlikely(map_value[k][i][0] == ((uint8_t)k21))) {
                        // Searching in k3 table
                        uint64_t b = map_value[k][i][1] + bucket;
                        int64_t k3 = ((int64_t)k03s[a] << 8) | cands[1][b].shifted.p8[2];
                        if (likely(idx3[k3] != -128)) {
                            int64_t d = idx3[k3] + k3;
                            while (likely(key_u24(&cands[3][d]) == k3)) {
                                if (unlikely(k13s[b] == k31s[d] && k23s[c] == k32s[d])) {
                                    // Found !!!!!!!
                                    #pragma omp critical
                                    {
                                        if (count < output_limit) {
                                            uint64_t idxs[4] = {a, b, c, d};
                                            uint8_t recovered_key[16];
                                            for (int i=0; i<4; i++) {
                                                *(uint32_t*)&recovered_key[i * 4] = cands[i][idxs[i]].column.u32;
                                            }
                                            memcpy(output + count * 16, recovered_key, 16);
                                            count += 1;
                                        }
                                    }
                                }
                                d++;
                            }
                        }
                    }
                }
            }
        }
    }

    free(idx3);
    free(k02s);
    free(k12s);
    free(k21s);
    free(k03s);
    free(k13s);
    free(k23s);
    free(k30s);
    free(k31s);
    free(k32s);

    return count;
}
