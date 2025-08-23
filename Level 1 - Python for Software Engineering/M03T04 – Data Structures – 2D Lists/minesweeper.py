

def minesweeper_numbers(grid):
    """
    Given a 2D list grid of '#' (mine) and '-' (safe), return a new grid where
    each '-' is replaced by the count of adjacent mines (including diagonals).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Helper function to count the number of mines around a given cell (i, j)
    # It checks all 8 neighboring cells and returns the count of '#' found
    def count_mines(i, j):
        return sum(
            1
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if not (dx == 0 and dy == 0)  # Skip the cell itself
            and 0 <= i + dx < rows        # Stay within row bounds
            and 0 <= j + dy < cols        # Stay within column bounds
            and grid[i + dx][j + dy] == '#'
        )

    # Build the result grid using nested list comprehensions
    # For each cell, if it's a mine, keep '#', otherwise replace with the count
    return [
        [
            '#' if grid[i][j] == '#'
            else str(count_mines(i, j))
            for j in range(cols)
        ]
        for i in range(rows)
    ]


if __name__ == "__main__":
    # Example 2D grid: '#' = mine, '-' = safe
    sample_grid = [
        ['#', '-', '#', '-'],
        ['-', '-', '-', '-'],
        ['-', '#', '#', '-'],
        ['-', '-', '-', '-']
    ]

    print("Original grid:")
    for row in sample_grid:
        print(' '.join(row))

    # Generate grid with mine counts
    numbered_grid = minesweeper_numbers(sample_grid)
    print("\nGrid with numbers:")
    for row in numbered_grid:
        print(' '.join(row))