def valid_row(row, grid):
    temp = grid[row]
    # Removing 0's.
    temp = list(filter(lambda a: a != 0, temp))
    # Checking for invalid values.
    if any(0 > i > 9 for i in temp):
        print("Invalid value")
        return -1
    # Checking for repeated values.
    elif len(temp) != len(set(temp)):
        return 0
    else:
        return 1


def valid_col(col, grid):
    # Extracting the column.
    temp = [row[col] for row in grid]
    # Removing 0's.
    temp = list(filter(lambda a: a != 0, temp))
    # Checking for invalid values.
    if any(0 > i > 9 for i in temp):
        print("Invalid value")
        return -1
    # Checking for repeated values.
    elif len(temp) != len(set(temp)):
        return 0
    else:
        return 1


def valid_subsquares(grid):
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            temp = []
            for r in range(row, row +3):
                for c in range(col, col +3):
                    if grid[r][c] != 0:
                        temp.append(grid[r][c])
            # Checking for invalid values.
            if any(0 > i > 9 for i in temp):
                print("Invalid value")
                return -1
            # Checking for repeated values.
            elif len(temp) != len(set(temp)):
                return 0
    return 1


# Function to check if the board invalid.
def valid_board(grid):
    for i in range(9):
        res1 = valid_row(i, grid)
        res2 = valid_col(i, grid)

        if res1 < 1 or res2 < 1:
            return False

    res3 = valid_subsquares(grid)
    if res3 < 1:
        return False
    else:
        return True


M = 9

def check(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False

    for x in range(9):
        if grid[x][col] == num:
            return False

    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True


def solve(grid, row, col):
    if not valid_board(grid):
        return False
    if row == M - 1 and col == M:
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return solve(grid, row, col + 1)
    for num in range(1, M + 1, 1):

        if check(grid, row, col, num):

            grid[row][col] = num
            if solve(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False


def generate():
    base = 3
    side = base * base

    # pattern for a baseline valid solution
    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample
    def shuffle(s): return sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = squares * 3 // 4 - 6
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board
