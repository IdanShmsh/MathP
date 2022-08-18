def for_each(func,range_end=50, range_start=0):
    for i in range(range_start,range_end):
        if is_prime(i):
            func(i)

def for_each_of_n(func,num):
    i = 0
    p_count = 0
    while True:
        if is_prime(i):
            func(i)
            p_count += 1
        i += 1
        if p_count >= num:
            return

def is_prime(x):
    if x <= 1: return False
    for i in range(2, int(x**0.5)):
        if x%i == 0:
            return False
    return True

def count(range_end=50, range_start=0):
    n = 0
    for i in range(range_start,range_end):
        if is_prime(i):
            n += 1
    return n