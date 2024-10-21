def path(n, blocks, start, blocked_coords):
    grid = [[0] * n for _ in range(n)]
    for block in blocks:
        grid[block[0]][block[1]] = 1
    for blocked in blocked_coords:
        grid[blocked[0]][blocked[1]] = 2

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    queue = [((start[0], start[1]), [(start[0], start[1])], set(blocks))]
    visited = set([(start[0], start[1], tuple(blocks))])

    while queue:
        (x, y), path, remaining_blocks = queue.pop(0)
        if not remaining_blocks:
            return path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            next = (nx, ny, tuple(sorted(remaining_blocks)))
            if (
                0 <= nx < n
                and 0 <= ny < n
                and grid[nx][ny] != 2
                and next not in visited
            ):
                if (nx, ny) in remaining_blocks:
                    new_remaining_blocks = remaining_blocks - {(nx, ny)}
                else:
                    new_remaining_blocks = remaining_blocks
                visited.add(next)
                queue.append(((nx, ny), path + [(nx, ny)], new_remaining_blocks))
    return []


n = 5
blocks = [(1, 2), (2, 2), (3, 2), (2, 3), (2, 1)]
blocked = [(0, 2), (4, 2)]
start = (0, 0)
result = path(n, blocks, start, blocked)
print(result)
