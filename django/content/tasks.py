from __future__ import absolute_import
from celery import shared_task

def is_prime(num):
    for j in range(2,num):
        if (num % j) == 0:
            return False
    return True

@shared_task
def prime_number(low,high):
    primes = 0
    if low < 2:
        start = 2
    else:
        start = low

    end = high + 1
    for p in range(start, end):
        if is_prime(p):
            primes += 1
    #return primes
    print("%s Primenumbers between %s and %s" %(primes, low, high))
