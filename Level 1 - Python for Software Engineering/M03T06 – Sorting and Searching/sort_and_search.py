number_list = [27, -3, 4, 5, 35, 2, 1, -40, 7, 18, 9, -1, 16, 100]

# a linear search function is appropriate 

def linear_search(items, target):
    for index, item in enumerate(items):
        if item == target:
            return index
    return None

target = 9
result = linear_search(number_list, target)
if result is not None:
    print(f"Item {target} found at index: {result}")
else:
    print(f"Item {target} not found in the list.")
# the linear search function works well for unsorted lists

# insertion sort function

def insertion_sort(arr):
    # Traverse from the second element to the end of the list
    for i in range(1, len(arr)):
        key = arr[i]  # The element to be inserted into the sorted part
        j = i - 1
        # Move elements of arr[0..i-1], that are greater than key, 
        # one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# applying insertion sort to the number_list
insertion_sort(number_list)
print("Sorted list using insertion sort:") 
print(number_list) 

# implimenting binary search function

def binary_search(items, target):
    low, high = 0, len(items) - 1

    # keep iterating until the low and high cross
    while low <= high:
        # find midpoint
        mid = (low + high) // 2

        #if item is found at midpoint, return its index
        if items[mid] == target:
            return mid
        # else, if item at midpoint is less than target,
        # search the second half of the list
        elif items[mid] < target:
            low = mid + 1
        # else, search the first half of the list
        else: 
            high = mid - 1

    # return none if the target item is not found
    return None

# Use the already sorted number_list for binary search
target_item = 9
result = binary_search(number_list, target_item)
if result is not None:
    print(f"Item {target_item} found at index {result}.")
else:
    print(f"Item {target_item} not found in the list.")

# i can use the binary search function to Find a specific value in a sorted 
# database or spreadsheet.





