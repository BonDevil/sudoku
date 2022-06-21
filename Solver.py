size = 9

def checker(grid, row, col, num):
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
    if row == size - 1 and col == size:
        return True
    if col == size:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return solve(grid, row, col + 1)
    for num in range(1, size + 1, 1):

        if checker(grid, row, col, num):

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
