import random

def generate_maze(width, height):
    maze = [["x"] * (2 * width + 1) for _ in range(2 * height + 1)]
    stack = []
    visited = set()

    def carve(x, y):
        maze[y][x] = " "
        visited.add((x, y))

        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited and 0 <= nx < 2 * width and 0 <= ny < 2 * height:
                maze[y + dy // 2][x + dx // 2] = " "
                stack.append((nx, ny))
                carve(nx, ny)

    start_x, start_y = random.randrange(0, width) * 2, random.randrange(0, height) * 2
    carve(start_x, start_y)
    maze[start_y][start_x] = "S"  # Start point
    maze[2 * height - 1][2 * width - 1] = "E"  # End point

    return maze

def print_maze(maze):
    for row in maze:
        print("".join(row))

# Example usage:
width = 30
height = 25
maze = generate_maze(width, height)
print_maze(maze)
