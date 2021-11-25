// nvcc -O3 main.cu && time ./a.out
#include <cstdio>
#include <cstdint>
#include <cassert>
#include <cuda_runtime.h>
#include <unordered_map>
#include <map>
#include <algorithm>
#include <vector>
#include <sys/time.h>

#include <thrust/sequence.h>
#include <thrust/execution_policy.h>
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>
#include <thrust/copy.h>
#include <thrust/fill.h>


using namespace std;

// Config

// GPU config
// #thread per block = warp size
#define THREAD_NUM 32
// #step per kernel invocation
#define LOOP_COUNT 1024

// Search config
// Search for 2^MAX_STEP_B steps (45 tooks at most 30min on T4)
// #define MAX_STEP_B 45
#define MAX_STEP_B 45
// Save approx 2^MAX_TRACE_B traces (26 tooks about 5GB)
// #define MAX_TRACE_B 26
#define MAX_TRACE_B 26
// Split to MAX_ROUND and search for collisions in the available traces after each round
#define MAX_ROUND 10

#define HASHBITS 64

#define MAX_STEP (1ULL<<MAX_STEP_B)
#define SHIFT (31 - (MAX_STEP_B - MAX_TRACE_B))
#define is_dis(x) (! (((uint32_t)(x)<<SHIFT)) )
#define HSHIFT (64 - HASHBITS)

static_assert(SHIFT >= 0);
static_assert(HSHIFT >= 0);


// Helpers

#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)

#define chkCuda(code) { _chkCuda((code), __FILE__, __LINE__); }
static inline void _chkCuda(cudaError_t code, const char *file, int line) {
   if (code != cudaSuccess) {
      fprintf(stderr,"\nCUDA Runtime Error: %s @ %s:%d\n", cudaGetErrorString(code), file, line);
      exit(code);
   }
}

#define FUNC __host__ __device__ static inline
#ifdef __CUDA_ARCH__
#define CONSTANT __constant__ const
#else
#define CONSTANT const
#endif

FUNC uint64_t xrand(uint64_t x) {
    x ^= x >> 12; // a
    x ^= x << 25; // b
    x ^= x >> 27; // c
    return x * 0x2545f4914f6cdd1dULL;
}


// Function config
typedef uint32_t state_t[16];

const uint32_t CHUNK_START         = 1 << 0;
const uint32_t CHUNK_END           = 1 << 1;
const uint32_t ROOT                = 1 << 3;
const uint32_t KEYED_HASH          = 1 << 4;

CONSTANT uint32_t IV[8] = {
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
};

CONSTANT uint32_t MSG_PERMUTATION[16] = {2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8};

// Rotate right
FUNC uint32_t blake3_ror (const uint32_t x, const uint32_t s) {
    return (x >> s) | (x << (32 - s));
}

// The mixing function, G, which mixes either a column or a diagonal.
FUNC void blake3_g(state_t& state, uint32_t a, uint32_t b, uint32_t c, uint32_t d, uint32_t mx, uint32_t my) {
    state[a] = state[a] + state[b] + mx;
    state[d] = blake3_ror(state[d] ^ state[a], 16);
    state[c] = state[c] + state[d];
    state[b] = blake3_ror(state[b] ^ state[c], 12);
    state[a] = state[a] + state[b] + my;
    state[d] = blake3_ror(state[d] ^ state[a], 8);
    state[c] = state[c] + state[d];
    state[b] = blake3_ror(state[b] ^ state[c], 7);
}

FUNC void blake3_round(state_t& state, state_t& m) {
    // Mix the columns.
    blake3_g(state, 0, 4, 8, 12, m[0], m[1]);
    blake3_g(state, 1, 5, 9, 13, m[2], m[3]);
    blake3_g(state, 2, 6, 10, 14, m[4], m[5]);
    blake3_g(state, 3, 7, 11, 15, m[6], m[7]);
    // Mix the diagonals.
    blake3_g(state, 0, 5, 10, 15, m[8], m[9]);
    blake3_g(state, 1, 6, 11, 12, m[10], m[11]);
    blake3_g(state, 2, 7, 8, 13, m[12], m[13]);
    blake3_g(state, 3, 4, 9, 14, m[14], m[15]);
}

FUNC void blake3_permute(state_t& m) {
    state_t tmp;
    for (int i=0; i<16; i++) {
        tmp[i] = m[MSG_PERMUTATION[i]];
    }
    memcpy(m, tmp, sizeof(tmp));
}

FUNC void blake3(uint32_t *key, state_t& block, uint32_t block_len) {
    uint32_t flags = KEYED_HASH | CHUNK_START | CHUNK_END | ROOT;
    state_t state = {
        key[0], key[1], key[2], key[3], key[4], key[5], key[6], key[7], 
        IV[0], IV[1], IV[2], IV[3], 0, 0, block_len, flags,
    };

    blake3_round(state, block); // round 1
    blake3_permute(block);
    blake3_round(state, block); // round 2
    blake3_permute(block);
    blake3_round(state, block); // round 3
    blake3_permute(block);
    blake3_round(state, block); // round 4
    blake3_permute(block);
    blake3_round(state, block); // round 5
    blake3_permute(block);
    blake3_round(state, block); // round 6
    blake3_permute(block);
    blake3_round(state, block); // round 7

    for (int i=0; i<8; i++) {
        block[i] = state[i] ^ state[i + 8];
        block[i+8] = state[i + 8] ^ key[i];
    }
}

FUNC uint64_t step(uint64_t k) {
    uint32_t key[8] = { 1768647031, 1768187248, 1919888993, 1769418599, 1412393323, 1768843634, 538999156, 538976288 };

    state_t block = { (uint32_t)k, (uint32_t)(k>>32), 0 };
    blake3((uint32_t*)key, block, 8);
    return ((((uint64_t)block[1] << 32) | block[0]) << HSHIFT) >> HSHIFT;
}


// Main algo

struct trace_t {
    uint64_t val;
    uint64_t end;
    uint64_t len;
};

struct cut_t {
    uint64_t val;
    uint64_t len;
};

__device__ int _count;

__global__ void init (uint64_t seed, trace_t* A, uint64_t n) {
    uint64_t tid = threadIdx.x + blockIdx.x * blockDim.x;
    if (tid >= n) return;
    auto&& X = A[tid];

    _count = 0;
    uint64_t x = xrand(seed + xrand(tid) + xrand(clock64()));
    X = {.val=x, .end=x, .len=0};
}

__global__ void gen_traces (trace_t* A, trace_t* O, uint64_t n) {
    uint64_t tid = threadIdx.x + blockIdx.x * blockDim.x;
    if (tid >= n) return;
    auto&& X = A[tid];

    uint64_t x = X.end, l = X.len;

    for (int i=0; i<LOOP_COUNT; i++) {
        // Step x
        x = step(x); l++;

        // Break the loop works much faster than start a new trace on pre-Volta GPU. (2x)
        // Search for distinguished point
        if (unlikely(is_dis(x))) { break; }
    }

    __syncwarp();

    X.end = x;
    X.len = l;

    if (unlikely(is_dis(x))) {
        // output result
        int idx = atomicAdd(&_count, 1);

        // check overflow
        if (likely(idx < n)) {
            O[idx] = X;
        }

        // new trace
        x = xrand(x + xrand(tid) + xrand(clock64()));
        X = {.val=x, .end=x, .len=0};
    }
}

__global__ void cut_traces (cut_t* C, uint64_t n) {
    uint64_t tid = threadIdx.x + blockIdx.x * blockDim.x;
    if (tid >= n) return;
    auto&& X = C[tid];

    uint64_t x = X.val, l = X.len;

    while (l--) { x = step(x); }

    __syncwarp();

    X.val = x;
}

uint64_t timer(bool reset=false) {
    static struct timeval tv_start, tv_end;

    if (tv_start.tv_sec == 0 || reset) {
        gettimeofday(&tv_start,NULL);
    }

    gettimeofday(&tv_end,NULL);
    uint64_t start = 1000000 * tv_start.tv_sec + tv_start.tv_usec;
    uint64_t end = 1000000 * tv_end.tv_sec + tv_end.tv_usec;
    return end - start;
}

struct tuple_hash : public unary_function<tuple<uint64_t, uint64_t>, size_t> {
    size_t operator()(const tuple<uint64_t, uint64_t>& k) const {
        return xrand(xrand(get<0>(k)) + xrand(get<1>(k)));
    }
};

unordered_map<uint64_t, map<uint64_t, uint64_t> > traces;
unordered_map<tuple<uint64_t, uint64_t>, uint64_t, tuple_hash> cut_cache;
uint64_t tcount = 0;
uint64_t steps = 0;
int done = 0;

void print_time(uint64_t x) {
    uint64_t s = x / 1e6;
    uint64_t m = s / 60;
    uint64_t h = m / 60;
    fprintf(stderr, "%02u:%02u:%02u", h, m%60, s%60);
}

void print_dur(double x, const char* suffix) {
    if (x < 1e3) {fprintf(stderr, "%8.2lf us%s", x, suffix); return;}
    if (x < 1e6) {fprintf(stderr, "%8.2lf ms%s", x / 1e3, suffix); return;}
    if (x < 6e7) {fprintf(stderr, "%5.2lf s%s", x / 1e6, suffix); return;}
    if (x < 36e8) {fprintf(stderr, "%5.2lf m%s", x / 6e7, suffix); return;}
    fprintf(stderr, "%5.2lf h%s", x / 36e8, suffix); return;
}

void stats(bool force=false) {
    static uint64_t last_dur = 0;
    uint64_t dur = timer();
    if (force || (dur >> 16) != (last_dur >> 16)) {
        double prog = (double) steps / MAX_STEP;
        uint64_t eta = (double)dur / prog;

        fprintf(stderr, "\r%6.2lf%% [", prog * 100);
        print_time(dur);
        fprintf(stderr, " / ");
        print_time(eta);
        fprintf(stderr, "] %.2lfG steps, %llu traces, %llu groups, ", 
            (double) steps / 1e9,
            tcount,
            traces.size()
        );
        print_dur((double)dur / tcount, "/T, ");
        print_dur((double)dur / traces.size(), "/G, ");
        fprintf(stderr, "%.2lf GS/s", (double)steps / dur / 1000);
        last_dur = dur;
    }
}

int main() {
    int ngpu = 0;
    cudaGetDeviceCount(&ngpu);
    fprintf(stderr, "[+] GPU Count: %lld\n", ngpu);
    if(ngpu == 0) { exit(0); }

    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, 0);
    fprintf(stderr, "[+] SM Count: %llu\n", prop.multiProcessorCount);
    uint64_t batch = prop.multiProcessorCount * 128 * 4;
    fprintf(stderr, "[+] Batch size: %llu\n", batch);
    uint64_t block_num = (batch + THREAD_NUM - 1) / THREAD_NUM;
    fprintf(stderr, "[+] Blocks: %llu\n", block_num);

    trace_t *O = new trace_t[batch], *_O, *_A;
    cut_t *C = new cut_t[batch], *_C;

    chkCuda( cudaMalloc(&_O, sizeof(_O[0]) * batch) );
    chkCuda( cudaMalloc(&_A, sizeof(_A[0]) * batch) );
    chkCuda( cudaMalloc(&_C, sizeof(_C[0]) * batch) );

    fprintf(stderr, "[*] Initializing\n");
    init<<<block_num, THREAD_NUM>>>(time(NULL), _A, batch);
    chkCuda( cudaPeekAtLastError() );
    chkCuda( cudaDeviceSynchronize() );

    fprintf(stderr, "[*] Start searching\n");

    timer();

    for (int round=0; !done && round<MAX_ROUND; round++) {
        while (steps < MAX_STEP * (round + 1) / MAX_ROUND) {
            gen_traces<<<block_num, THREAD_NUM>>>(_A, _O, batch);
            chkCuda( cudaPeekAtLastError() );
            chkCuda( cudaDeviceSynchronize() );

            // Retrieve results
            int count;
            chkCuda( cudaMemcpyFromSymbol(&count, _count, sizeof(count)) );
            assert( count <= batch );
            if (count) {
                chkCuda( cudaMemcpy(O, _O, sizeof(trace_t) * count, cudaMemcpyDeviceToHost) );

                tcount += count;

                // Save traces
                for (int i=0; i<count; i++) {
                    auto&& X = O[i];
                    steps += X.len;
                    traces[X.end][X.val] = X.len;
                }

                // Reset buffer
                count = 0;
                chkCuda( cudaMemcpyToSymbol(_count, &count, sizeof(count)) );
            }

            stats();
        }

        stats(true);
        fprintf(stderr, "\n");

        unordered_map<uint64_t, map<uint64_t, uint64_t> > groups;
        for (auto& it : traces) { if (it.second.size() > 2) groups[it.first] = it.second; }
        fprintf(stderr, "%16llu groups", groups.size());

        vector<trace_t> cached;
        vector<trace_t> cutv;
        vector<cut_t> cuts;
        thrust::host_vector<uint64_t> lens;
        while(!done && groups.size()) {
            done = true;

            // Split groups with too many collision
            uint64_t cut_steps = 0;
            for (auto& it : groups) {
                auto&& g = it.first;
                auto&& A = it.second;

                uint64_t maxlen = 0;
                for (auto& it : A) { maxlen = max(maxlen, it.second); }

                if (maxlen == 1) { continue; } // finished
                done = false;

                uint64_t cutpoint = 1ULL << (63 - __builtin_clzll(maxlen-1));
                assert(cutpoint < maxlen);
                assert(cutpoint >= maxlen / 2);

                map<uint64_t, uint64_t> B = move(A);
                assert(A.size() == 0);
                for (auto& it : B) {
                    uint64_t v = it.first;
                    uint64_t len = it.second;
                    if (len > cutpoint) { // cut
                        uint64_t s = len - cutpoint;
                        auto&& it = cut_cache.find({v, s});
                        if (it != cut_cache.end()) {
                            uint64_t m = it->second;
                            cached.push_back({.val=v, .end=m, .len=s});
                            A[m] = cutpoint;
                        } else {
                            cutv.push_back({.val=v, .end=g, .len=len});
                            cuts.push_back({.val=v, .len=s});
                            lens.push_back(s);
                            cut_steps += s;
                        }
                    } else { // keep
                        A[v] = len;
                    }
                }
            }
            if (done) break;
            for (auto&& X : cached) { groups[X.end][X.val] = X.len; }
            cached.clear();

            fprintf(stderr, ", %16d traces, %16llu steps.", cuts.size(), cut_steps);

            thrust::host_vector<uint64_t> idx;
            {
                thrust::device_vector<uint64_t> _lens = lens;
                thrust::device_vector<uint64_t> _idx(lens.size());
                thrust::sequence(_idx.begin(), _idx.end());
                thrust::sort_by_key(_lens.begin(), _lens.end(), _idx.begin());
                chkCuda( cudaDeviceSynchronize() );
                idx = _idx;
            }
            lens.clear();
            fprintf(stderr, ".     ");

            for (uint64_t i=0; i<cuts.size(); i+=batch) {
                fprintf(stderr, "\b\b\b\b%3llu%%", i * 100 / cuts.size());
                uint64_t n = min((uint64_t)cuts.size() - i, (uint64_t)batch);
                for (int k=0; k<n; k++) { C[k] = cuts[idx[i+k]]; }
                chkCuda( cudaMemcpy(_C, C, sizeof(cut_t) * n, cudaMemcpyHostToDevice) );
                chkCuda( cudaDeviceSynchronize() );

                cut_traces<<<block_num, THREAD_NUM>>>(_C, n);
                chkCuda( cudaPeekAtLastError() );
                chkCuda( cudaDeviceSynchronize() );

                chkCuda( cudaMemcpy(C, _C, sizeof(cut_t) * n, cudaMemcpyDeviceToHost) );
                chkCuda( cudaDeviceSynchronize() );
                for (int k=0; k<n; k++) { cuts[idx[i+k]] = C[k]; }
            }
            fprintf(stderr, "\b\b\b\b\b.     \b\b\b\b\b");

            {
                for (int i=0; i<cuts.size(); i++) {
                    auto&& X = cutv[i];
                    auto&& C = cuts[i];
                    groups[C.val][X.val] = C.len;
                    groups[X.end][C.val] = X.len - C.len;
                    cut_cache[{X.val, C.len}] = C.val;
                }
            }
            cutv.clear();
            cuts.clear();

            fprintf(stderr, " done\n");
            steps += cut_steps;

            // Remove groups without enough collision
            vector<uint64_t> remove;
            for (auto& it : groups) { if (it.second.size() <= 2) remove.push_back(it.first); }
            for (auto g : remove) { groups.erase(g); }
            fprintf(stderr, "%16llu groups", groups.size());
        }
        fprintf(stderr, "\n");

        if (done && groups.size()) {
            for (auto& it : groups) {
                auto&& g = it.first;
                auto&& A = it.second;
                uint64_t maxlen = 0;
                for (auto& it : A) { maxlen = max(maxlen, it.second); }
                if (maxlen != 1) { continue ;}

                fprintf(stderr, "%016llx:\n", __builtin_bswap64(g));
                for (auto& it : A) {
                    uint64_t v = it.first;
                    fprintf(stderr, "  %016llx -> %016llx\n", __builtin_bswap64(v), __builtin_bswap64(step(v)));
                }
            }
            break;
        }
    }
}
