# Task Info
secure_hash v2 - 10 solves - 488 pts
> It has come to our attention that the released version of our
> SecureHash class was in fact not completely secure.
> We're deeply sorry about that,
> and after whipping our sole developer an appropriate number of
> times we now proudly present SecureHash v2.
> It features twice as much security as before,
> and is now certified to be absolutely free of bugs.
> Update: the binary was compiled with g++ and libstdc++, 64bit

## Time
1 hour

# Solution
## TL;DR
1. Calculate the bucket number of <root, pwd>
2. Search 1000 credentials has same bucket number and register them.
3. Login with <root, pwd>


The task has two operation, register and login.
It store the credential using:
```
sha512(sha512(name) + password)
```
As far as I know, no collision attack available on this digest method.
But the server has some interesting code when it search for hash:
```C++
auth_result lookup_keyvalue(const std::string& name, const std::string& password) {
    std::string digest = sha512sum(name, password);
    size_t bucket = values.bucket(digest);

    auto it = values.begin(bucket), end = values.end(bucket);
    size_t iterations = 0;
    size_t MAX_ITERATIONS = 1000;

    while (it != end) {
        if (*it++ == digest)
            return AUTH_SUCCESS; // 1

        // Avoid DoS attacks by fixing upper time limit.
        if (iterations++ >= MAX_ITERATIONS)
            return AUTH_TIMEOUT; // 2
    }

    return AUTH_FAILURE; // 0
}
...
            if (table.lookup_keyvalue(name, password)) {
                // login successfully, check root and print flag
...
```
We can login when it reach the limit of iterations,
Search for 1000 credentials with same bucket number as `root, pwd`.
register them and login with `root, pwd` to get the flag.
Here's the [code](dos.cpp).
