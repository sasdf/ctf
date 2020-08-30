#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include <ctype.h>
#include "rng.h"
#include "api.h"


FILE* sig_file;

int main() {
    printf("SPX_BYTES = %u\n", SPX_BYTES);
    int ret;
    FILE* pub_file = fopen("pub.bin", "r");
    assert (pub_file != NULL);
    uint8_t pk[4096];
    memset(pk, 0, 4096);
    ret = fread(pk, 16, 1, pub_file);
    assert (ret == 1);
    fclose(pub_file);
    uint8_t sk[4096];
    memcpy(sk+2*SPX_N, pk, 16);


    sig_file = fopen("sigs.bin", "r");
    assert (sig_file != NULL);

    for (int i=0; i<10000; i++) {
        uint8_t sig[4096];
        ret = fread(sig, 1280, 1, sig_file);
        assert (ret == 1);

        uint8_t m[4096] = "abc";
        uint8_t sm[4096];
        memcpy(sm, sig, 1280);
        memcpy(sm+1280, m, 3);

        uint8_t buf[4096];
        buf[0] = 0;
        unsigned long long blen;
        
        ret = crypto_sign_open(buf, &blen, sm, 1280 + 3, pk);
        assert (ret == 0);
        printf("%d\n", i);
        // printf("result = %d\n", ret);
        // printf("buf = %s\n", buf);
        // printf("blen = %llu\n", blen);
        // puts("");
    }

    extern int loading_sk;
    loading_sk = 0;

    {
        uint8_t sig[4096];
        ret = fread(sig, 1280, 1, sig_file);
        assert (ret == 1);

        uint8_t m[4096] = "opensesame";
        int mlen = 10;
        uint8_t sm[4096];
        memset(sm, 0, 1280);
        memcpy(sm+1280, m, mlen);

        uint8_t buf[4096];
        buf[0] = 0;
        unsigned long long blen;
        
        ret = crypto_sign_open(buf, &blen, sm, 1280 + mlen, pk);
        printf("result = %d\n", ret);
        printf("buf = %s\n", buf);
        printf("blen = %llu\n", blen);

        puts("sig");
        for (int i=0; i<1280; i++) {
            printf("%02x", sm[i]);
        }
        puts("");
    }

    // fseek(sig_file, 1280, SEEK_SET);
    // for (int i=0; i<10; i++) {
    //     printf("start = %ld\n", ftell(sig_file));
    //     ret = crypto_sign(buf, &blen, m, 3, sk);
    //     printf("end = %ld\n", ftell(sig_file));
    //     printf("result = %d\n", ret);
    //     // printf("buf = %s\n", buf);
    //     printf("blen = %llu\n", blen);
    // }

    fclose(sig_file);
    return 0;
}
