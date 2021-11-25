bits = 1024


while True:
    p = 2 * random_prime(2^bits) + 1
    print(p)
    if is_pseudoprime(p) and is_prime(p):
        break

print('p =', p)
print('s =', randrange(2^100))
