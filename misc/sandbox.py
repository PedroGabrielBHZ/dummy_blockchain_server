# name = "Joseph"
# age = 25

# print(f'I am {name} and I am {age} years old')

import math

my_numbers = [i**2 for i in range(10)]
my_numbers= list(map(math.sqrt, my_numbers))
print(my_numbers)