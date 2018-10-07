#include <openssl/evp.h>

#include <unordered_set>
#include <iostream>
#include <fstream>

#include <unistd.h>

// "I hereby certify that this software is secure and does
//  not contain any bugs."
//             - Pope Alexander VI (1431-1503)


// TODO - Make an #ifdef to detect openssl/libressl.
//#define EVP_CREATE_FN() EVP_MD_CTX_new()
//#define EVP_DESTROY_FN(x) EVP_MD_CTX_free(x)
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

    auth_result lookup_keyvalue(const std::string& name, const std::string& password) {
        std::string digest = sha512sum(name, password);
        size_t bucket = values.bucket(digest);

        auto it = values.begin(bucket), end = values.end(bucket);
        size_t iterations = 0;
        size_t MAX_ITERATIONS = 1000;

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

    std::ifstream ifs("./flag.txt");
    std::string flag;
    ifs >> flag;

    SecureHashtable table;
    table.insert_keyvalue("root", flag);

    while (true) {
        // usleep(1000);

        int choice;
        std::string name, password;
        printf("Main menu:\n1 - Register new user\n2 - Login\n");
        std::cin >> choice;

        printf("Name: ");
        std::cin >> name;

        printf("Password: ");
        std::cin >> password;

        if (choice == 1) {
            if (name == "root") {
                            printf("You are not root!\n");
                continue;
            }
            table.insert_keyvalue(name, password);
        } else if (choice == 2) {
            if (table.lookup_keyvalue(name, password)) {
                printf("Success! Logged in as %s\n", name.c_str());
                if (name == "root") {
                    printf("You win, the flag is %s\n", flag.c_str());
                    return 0;
                }
            } else {
                printf("Invalid credentials!\n");
            }
        } else {
            printf("Invalid choice!\n");
        }
    }
}
