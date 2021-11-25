#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <fcntl.h>
#include <unistd.h>

#include "hash.h"


int main () {
    int ret;
    uint8_t final_state[16];

    ret = read(0, final_state, 16);
    assert (ret == 16);

    uint8_t output[16 * 16];
    size_t cnt = hash_inverse(final_state, output, sizeof(output));

    ret = write(1, output, cnt * 16);
    assert (ret == cnt * 16);
}
