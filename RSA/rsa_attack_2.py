import rsa
import random
import math
import time

 # n rsa modulus, d private exponent, e public exponent
def decryptionexp(n: int, d: int, e: int):
    # e*d - 1 = 2^r * m, m is odd, r >= 1
    sum_ed = e*d - 1

    r = 0
    m = e*d - 1
    while m % 2 == 0:
        m //= 2
        r += 1
  
    while True:        
        x = random.randint(1, n-1)
        if math.gcd(x, n) != 1:
            return x, 0 # risultato banale
        
        x_0 = pow(x, m, n)
        x_values = [x_0]
        
        for i in range(1, r + 1):
            x_next = pow(x_values[-1], 2, n)
            x_values.append(x_next)

        for j in range(1, len(x_values)):
            if x_values[j] == 1 and x_values[j - 1] != n - 1:
                factor = math.gcd(x_values[j - 1] + 1, n)
                if 1 < factor < n:
                    return factor, j

        
def test_rsa_decryption(nr_tests, nr_bits):
    iterations = nr_tests
    k = nr_bits

    n_list = []
    exec_time_list = []
    algorithm_iterations_list = []

    for i in range(iterations):
        print("Iteration", i)

        p = rsa.generate_prime(k)
        q = rsa.generate_prime(k)
        e, d, n = rsa.generate_key(p, q)
        n_list.append(n)

        start_time = time.perf_counter()
        factor, j = decryptionexp(n, d, e)
        end_time = time.perf_counter()

        exec_time = end_time - start_time
        exec_time_list.append(exec_time)
        algorithm_iterations_list.append(j)
    
    # calculate average execution time
    avg_exec_time = sum(exec_time_list) / iterations

    # calculate variance of execution time
    var_exec_time = 0
    for exec_time in exec_time_list:
        var_exec_time += (exec_time - avg_exec_time) ** 2
    var_exec_time /= iterations

    # calculate average algorithm iterations
    avg_algorithm_iterations = sum(algorithm_iterations_list) / iterations

    return avg_algorithm_iterations, var_exec_time, avg_exec_time

def display_results(avg_algorithm_iterations, var_exec_time, avg_exec_time, nr_tests, k):
    print(f"{'Metric':<30}{'Value':<20}")
    print("-" * 50)
    print(f"{'Number of Tests':<30}{nr_tests:<20}")
    print(f"{'Number of Bits':<30}{k:<20}")
    print(f"{'Average Algorithm Iterations':<30}{avg_algorithm_iterations:<20}")
    print(f"{'Average Execution Time':<30}{avg_exec_time:<20}")
    print(f"{'Time Variance':<30}{var_exec_time:<20}")



nr_tests = 100
k = 1024

avg_algorithm_iterations, var_exec_time, avg_exec_time = test_rsa_decryption(nr_tests, k)
display_results(avg_algorithm_iterations, var_exec_time, avg_exec_time, nr_tests, k)

    
    