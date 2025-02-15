print('Welcome to Prime Factor calculator!')

num = int(input("Enter a number: "))

def prime_factors(n):
  factors = []
  divisor = 2
  while divisor <= n:
    if n % divisor == 0:
      factors.append(divisor)
      n = n // divisor
    else:
      divisor += 1
  return factors

print(prime_factors(num))