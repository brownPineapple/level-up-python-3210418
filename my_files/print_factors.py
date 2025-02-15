print('Welcome to Prime Factor calculator!')

def prime_factors(n):
  factors = [] # Create an empty list for factors
  divisor = 2 # init divisor
  while divisor <= n: 
    if n % divisor == 0:
      factors.append(divisor) # if no remainder append factor list
      n = n // divisor # set n to the new value
    else:
      divisor += 1 # increment divisor
  return factors

num = int(input("Enter a number: "))

print(prime_factors(num))