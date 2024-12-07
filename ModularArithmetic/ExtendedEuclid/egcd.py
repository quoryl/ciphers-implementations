
a = 12
b = 30

def egcd(a, b):
    x = 1    
    u = 0    
    y = 0
    v = 1    
    while a != 0:
        q = b // a
        r = b % a
        s = x - q * u
        t = y - q * v
        b = a
        a = r
        x = u
        y = v
        u = s
        v = t
    gcd = b
    return gcd, x, y

print(egcd(a, b))