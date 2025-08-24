def find_largest(nums, idx=None):
    """
    Recursively find the largest number in a list of integers.
    Args:
        nums (list of int): The list of integers to search.
        idx (int, optional): The current index being checked. Defaults to last index.
    Returns:
        int: The largest number in the list.
    """
    if idx is None:
        # Starting recursion from the last index
        idx = len(nums) - 1
    if idx == 0:
        # Base case: only one element left
        return nums[0]
    # Compare the current element with the largest found in the rest of the list
    current = nums[idx]
    largest_in_rest = find_largest(nums, idx - 1)
    return current if current > largest_in_rest else largest_in_rest



# Example usage
if __name__ == "__main__":
    numbers = [7, 18, 2, 15, 11, 9]
    print(f"Largest number: {find_largest(numbers)}")
