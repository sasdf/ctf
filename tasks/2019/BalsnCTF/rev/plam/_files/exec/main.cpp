#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cassert>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>

#include <string>
#include <vector>
#include <map>

using namespace std;

typedef uint32_t ID;
typedef uint64_t Pair;

#define argStart 1
#define argEnd 65
#define absStart 65
#define absEnd 0x8000000
#define appStart 0x8000000
#define appEnd 0xfffffff
#define IDMASK 0xfffffff

#define isArg(x) (argStart <= x && x < argEnd)
#define isAbs(x) (absStart <= x && x < absEnd)
#define isApp(x) (appStart <= x && x < appEnd)

#define buildApp(a, b, i) ( (((Pair)i) << 56) | (((Pair)a) << 28) | (Pair)b )
#define getFunc(x) ((ID) (x >> 28) & IDMASK)
#define getParam(x) ((ID) (x) & IDMASK)
#define getDepth(x) ((ID) (x >> 56) & 0xff)
#define getAbsDef(x) (AbstractionDef[x - absStart])
#define getAppDef(x) (ApplicationDef[x - appStart])

vector<ID> AbstractionDef;
vector<Pair> ApplicationDef;
map<ID, ID> AbstractionMap;
map<Pair, ID> ApplicationMap;
map<Pair, ID> SubstitutionCache;
map<Pair, ID> ReductionCache;
map<ID, uint64_t> FreevarMap;

ID App (ID a, ID b) {
    Pair content = buildApp(a, b, 0);
    auto cache = ApplicationMap.find(content);
    if (cache != ApplicationMap.end()) {
        return cache->second;
    }
    ID id = ApplicationDef.size() + appStart;
    assert(id < appEnd);
    ApplicationDef.push_back(content);
    ApplicationMap[content] = id;
    FreevarMap[id] = FreevarMap[a] | FreevarMap[b];
    return id;
}

ID Abs (ID x) {
    auto cache = AbstractionMap.find(x);
    if (cache != AbstractionMap.end()) {
        return cache->second;
    }
    ID id = AbstractionDef.size() + absStart;
    assert(id < absEnd);
    AbstractionDef.push_back(x);
    AbstractionMap[x] = id;
    FreevarMap[id] = FreevarMap[x] >> 1;
    return id;
}

void show(ID x) {
    if (isArg(x)) {
        cout << x;
    } else if (isAbs(x)) {
        cout << "λ";
        show(getAbsDef(x));
    } else if (isApp(x)) {
        cout << "(";
        Pair p = getAppDef(x);
        show(getFunc(p));
        cout << " ";
        show(getParam(p));
        cout << ")";
    } else {
        cerr << "WTF";
        exit(1);
    }
}

ID substitute (ID x, ID v, uint64_t i) {
    if (!(i & FreevarMap[x])) {
        return x;
    }

    if (isArg(x)) {
        return v;
    }

    Pair p = buildApp(x, v, i);
    auto it = SubstitutionCache.find(p);
    if (it != SubstitutionCache.end()) {
        return it->second;
    }

    if (isAbs(x)) {
        ID ret = Abs(substitute(getAbsDef(x), v, i<<1));
        SubstitutionCache[p] = ret;
        return ret;
    }

    if (isApp(x)) {
        Pair p = getAppDef(x);
        ID a = substitute(getFunc(p), v, i);
        ID b = substitute(getParam(p), v, i);
        ID ret = App(a, b);
        SubstitutionCache[p] = ret;
        return ret;
    }
}

ID reduce (ID x) {
    assert(isApp(x));

    // Run through cached reduction chains
    ID y = x;
    auto it = ReductionCache.find(y);
    while (it != ReductionCache.end()) {
        y = it->second;
        it = ReductionCache.find(y);
    }

    // Shortcut cached reduction chains
    it = ReductionCache.find(x);
    while (it != ReductionCache.end()) {
        x = it->second;
        it->second = y;
        it = ReductionCache.find(x);
    }

    // Reduce
    assert(y == x);
    while (isApp(y)) {
        Pair p = getAppDef(y);
        ID f = getFunc(p);
        ID v = getParam(p);

        if (isApp(f)) {
            f = reduce(f);
        }

        if (isArg(f)) {
            cerr << "UnboundLocalError('Free variable')" << endl;
            abort();
        }

        assert(isAbs(f));

        ID z = substitute(getAbsDef(f), v, 1);
        ReductionCache[y] = z;
        y = z;
    }

    if (x != y) {
        ReductionCache[x] = y;
    }

    return y;
}


ID parse (const char* x, int* i, map<char, int> symtab) {
    assert(x[*i] == '(');
    (*i)++;

    int nargs = 0;
    if (x[*i] == '\\') {
        (*i)++;
        for(;x[*i] != '.'; (*i)++) {
            for (auto& x : symtab) {
                x.second++;
                assert(x.second < argEnd);
            }
            symtab[x[*i]] = 1;
            nargs++;
        }
        (*i)++;
    }

    ID ret = 0, cur = 0;
    for (;x[*i] != ')'; (*i)++) {
        if (x[*i] == ' ') {
            continue;
        } else if (x[*i] == '(') {
            cur = parse(x, i, symtab);
        } else {
            auto it = symtab.find(x[*i]);
            assert(it != symtab.end());
            cur = it->second;
        }
        if (ret == 0) {
            ret = cur;
        } else {
            ret = App(ret, cur);
        }
    }

    for (int i=0; i<nargs; i++) {
        ret = Abs(ret);
    }

    return ret;
}



int main (int argc, const char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input.plam>\n", argv[0]);
        exit(1);
    }

    for (uint64_t i=0; i<64; i++) {
        FreevarMap[i+1] = ((uint64_t)1 << i);
    }


    ID T = Abs(Abs(2));
    ID F = Abs(Abs(1));

    FILE* pFile = fopen(argv[1] , "rb");
    if (pFile==NULL) {fputs("File error", stderr); exit(1);}
    fseek(pFile, 0, SEEK_END);
    size_t lSize = ftell(pFile);
    rewind(pFile);
    char* buf = (char*) malloc (sizeof(char)*lSize);
    if (buf == NULL) {fputs("Memory error", stderr); exit(2);}
    size_t result = fread(buf, 1, lSize, pFile);
    if (result != lSize) {fputs("Reading error", stderr); exit(3);}
    fclose(pFile);
    
    int i=0;
    map<char, int> symtab;

    cerr << "[*] Parsing..." << endl;
    ID z = parse(buf, &i, symtab);
    cerr << "[+] # Abstraction: " << AbstractionDef.size() << endl;
    cerr << "[+] # Application: " << ApplicationDef.size() << endl;
    cerr << "[+] Result ID: " << z << endl;
    
    cerr << endl;
    cerr << "[*] Running..." << endl;
    z = reduce(z);
    cerr << "[+] # Abstraction: " << AbstractionDef.size() << endl;
    cerr << "[+] # Application: " << ApplicationDef.size() << endl;
    cerr << "[+] # Reduction: " << ReductionCache.size() << endl;
    cerr << "[+] Result ID: " << z << endl;
    cerr << "[+] Result Representation: " << endl;
    show(z); cout << endl;
    _Exit(0);
}
