
a = 5
b = 13

def egcd(a, b):
    x = 0    
    u = 1    
    y = 1
    v = 0    
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