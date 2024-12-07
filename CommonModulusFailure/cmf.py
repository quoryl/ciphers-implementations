
# rsa modulus
n = 1309914994772590863210166992356557234456075980579048604758768205496404269677841156459642052158879494989630338961154043468325508153199153204245943547981

e1 = 5
e2 = 13

# c1 = m^e1 mod n
c1 = 1208833588708967444709375

# c2 = m^e2 mod n
c2 = 411294544478239271886338859092185183748200324266700081787109375

# ricavare m, senza fattorizzare n, senza ricavare d

# identità di Bézout: a * x + b * y = gcd(a, b)
# e1 * x + e2 * y = 1
# c1^x * c2^y mod n = m^(e1 * x) * m^(e2 * y) mod n = m ^ (e1 * x + e2 * y) mod n = m mod n


# calcolare x, y
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    
g, x, y = egcd(e1, e2)
print("Computed g, x, y: ", g, x, y)

# calcolare m

m = pow(c1, x, n) * pow(c2, y, n) % n
print("Decrypted message: ", m)





