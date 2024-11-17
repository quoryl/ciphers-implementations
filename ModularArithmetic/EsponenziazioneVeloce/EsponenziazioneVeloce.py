b = 13
a = 3
m = 7

binary_representation = [int(c) for c in bin(b)[2:][::-1]]
indices = list(enumerate(binary_representation))

# a^b mod m
d = 1
for k in indices:
    two_power_k = pow(2, k[0]) * k[1] # 2^k * b_k    
    local_result = pow(a, two_power_k, m) # a^(2^k * b_k) mod m
    d = (d * local_result) % m
   

print(d)
