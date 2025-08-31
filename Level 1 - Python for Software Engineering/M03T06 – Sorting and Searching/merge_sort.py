def merge_sort_by_length(strings):
def merge_by_length(left, right):

# Merge Sort for Strings by Length (Longest to Shortest)

def merge_sort_by_length(strings):
    """
    Sorts a list of strings by their length in descending order (longest to shortest)
    using the merge sort algorithm.
    Args:
        strings (list): List of strings to sort.
    Returns:
        list: Sorted list of strings from longest to shortest.
    """
    if len(strings) <= 1:
        return strings
    mid = len(strings) // 2
    left = merge_sort_by_length(strings[:mid])
    right = merge_sort_by_length(strings[mid:])
    return merge_by_length(left, right)


def merge_by_length(left, right):
    """
    Merges two lists of strings into a single list, sorting by string length
    in descending order (longest to shortest).
    Args:
        left (list): First sorted list of strings.
        right (list): Second sorted list of strings.
    Returns:
        list: Merged and sorted list of strings.
    """
    result = []
    i = 0
    j = 0
    # Compare elements from both lists and append the longer string first
    while i < len(left) and j < len(right):
        if len(left[i]) >= len(right[j]):  # Longest first
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # Append any remaining elements from left or right
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Example string lists (unsorted, at least 10 elements each)
list1 = [
    "apple", "banana", "kiwi", "strawberry", "grape",
    "pineapple", "fig", "blueberry", "melon", "pear", "plum"
]
list2 = [
    "elephant", "dog", "cat", "hippopotamus", "ant",
    "giraffe", "lion", "tiger", "bear", "wolf", "zebra"
]
list3 = [
    "notebook", "pen", "eraser", "sharpener", "marker",
    "ruler", "calculator", "stapler", "paper", "folder", "scissors"
]

# Sort and print results for each list
for idx, test_list in enumerate([list1, list2, list3], 1):
    sorted_list = merge_sort_by_length(test_list)
    print(f"Sorted list {idx} (longest to shortest):\n{sorted_list}\n")
