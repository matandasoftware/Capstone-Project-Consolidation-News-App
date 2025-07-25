# a short zigzag program with 

# pseudo code

# 1. Using one for loop to print a zigzag pattern made of * 
# 2. The pattern should be columns of 8 *, 7 *, 5 *, 3 *, and 1 * characters respectively
# 3. This is achieved using two ranges: 8, 7, 5, 3, 1
# 4. The two ranges can be chained together if needed for a more complex pattern
# 5. The * character will be printed in a column with the number of * characters equal to the value in the list
# 6. The zigzag pattern will be printed to the console

# python code

""" import intertools to use a single for loop for range(1, 6, 1) and range(4, 1, -1) to print a zigzag pattern of * characters"""

import itertools as it
for i in it.chain(range(1, 6, 1), range(4, 1, -1)):
    print('*' * i)
