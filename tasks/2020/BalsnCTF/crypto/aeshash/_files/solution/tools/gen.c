#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <fcntl.h>
#include <unistd.h>

#include "hash.h"


uint8_t final_states[1024 * 16];
uint64_t depths[1024];
uint64_t nstates = 0;

int main () {
    // test();
    uint64_t target_hash = 0xdeadbeef01231337ULL;
    uint64_t target_depth = 3;

    nstates = 0;
    int urandom = open("/dev/urandom", O_RDONLY);
    for (int qaq=0; qaq<200; qaq++) {
        if (nstates == 0) {
            read(urandom, final_states, 16);
            *(uint64_t*)final_states = target_hash;
            nstates = 1;
            depths[0] = 0;
        }

        nstates -= 1;
        uint64_t depth = depths[nstates] + 1;
        uint8_t *final_state = &final_states[nstates * 16];

        uint8_t output[16 * 16];
        size_t cnt = hash_inverse(final_state, output, sizeof(output));
        memcpy(final_state, output, cnt*16);
        printf("Found %lu solutions\n", cnt);

        for (int i=0; i<cnt; i++) {
            uint8_t *state = &final_states[nstates * 16];

            printf("\n");
            for (int i=0; i<4; i++) {
                for (int j=0; j<4; j++) {
                    printf("0x%02x, ", state[i * 4 + j]);
                }
                printf("\n");
            }
            printf("\n");
            if (depth == target_depth) {
                printf("Done\n");
                exit(0);
            }

            depths[nstates++] = depth;
        }

        printf("Stack size: %d\n", nstates);
        printf("Current depth: %d\n", depth);
        printf("\n");
    }
}
