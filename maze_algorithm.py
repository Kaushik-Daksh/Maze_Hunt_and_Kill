
import pygame
import random
from collections import deque

# ---------------- SETTINGS ----------------

CELL_SIZE = 30
COLS = 25
ROWS = 18

WIDTH = COLS * CELL_SIZE
MAZE_HEIGHT = ROWS * CELL_SIZE
HUD_HEIGHT = 50
HEIGHT = MAZE_HEIGHT + HUD_HEIGHT

FPS = 60
GENERATION_SPEED = 120

# ---------------- COLORS ----------------

BACKGROUND = (25, 25, 30)
WALL_COLOR = (230, 230, 230)
HUD_COLOR = (40, 40, 48)
TEXT_COLOR = (255, 255, 255)

# ---------------- CELL ----------------


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.visited = False

        self.walls = {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True
        }


# ---------------- MAZE ----------------


class Maze:
    def __init__(self):
        self.grid = [
            [Cell(x, y) for x in range(COLS)]
            for y in range(ROWS)
        ]

        self.start = self.grid[0][0]
        self.end = self.grid[ROWS - 1][COLS - 1]

        self.finished = False
        self.valid = False

    # Get neighboring cells
    def get_neighbors(self, cell):
        neighbors = []

        x = cell.x
        y = cell.y

        directions = [
            (0, -1, "top"),
            (1, 0, "right"),
            (0, 1, "bottom"),
            (-1, 0, "left")
        ]

        for dx, dy, direction in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < COLS and 0 <= ny < ROWS:
                neighbor = self.grid[ny][nx]

                if not neighbor.visited:
                    neighbors.append((neighbor, direction))

        return neighbors

    # Remove the wall between two neighboring cells
    def remove_walls(self, cell1, cell2, direction):
        opposite = {
            "top": "bottom",
            "right": "left",
            "bottom": "top",
            "left": "right"
        }

        cell1.walls[direction] = False
        cell2.walls[opposite[direction]] = False

    # Hunt and Kill algorithm
    def generate(self):
        current = self.start

        while True:

            # ---------------- KILL PHASE ----------------

            while current:
                current.visited = True

                neighbors = self.get_neighbors(current)

                if neighbors:
                    neighbor, direction = random.choice(neighbors)

                    self.remove_walls(
                        current,
                        neighbor,
                        direction
                    )

                    current = neighbor

                else:
                    current = None

                yield

            # ---------------- HUNT PHASE ----------------

            found = False

            for y in range(ROWS):
                for x in range(COLS):

                    cell = self.grid[y][x]

                    if cell.visited:
                        continue

                    visited_neighbors = []

                    directions = [
                        (0, -1, "top"),
                        (1, 0, "right"),
                        (0, 1, "bottom"),
                        (-1, 0, "left")
                    ]

                    for dx, dy, direction in directions:
                        nx = x + dx
                        ny = y + dy

                        if 0 <= nx < COLS and 0 <= ny < ROWS:
                            neighbor = self.grid[ny][nx]

                            if neighbor.visited:
                                visited_neighbors.append(
                                    (neighbor, direction)
                                )

                    if visited_neighbors:
                        neighbor, direction = random.choice(
                            visited_neighbors
                        )

                        # Direction is from the unvisited cell
                        # towards its visited neighbor.
                        self.remove_walls(
                            cell,
                            neighbor,
                            direction
                        )

                        current = cell
                        found = True
                        break

                if found:
                    break

            # No unvisited cell has a visited neighbor.
            # The maze is complete.
            if not found:
                break

            yield

        # Create entrance and exit
        self.start.walls["top"] = False
        self.end.walls["bottom"] = False

        self.finished = True
        self.valid = self.validate()

        yield

    # Verify that the maze is perfect
    def validate(self):

        visited = set()
        queue = deque([(0, 0)])

        passages = 0

        # Count internal passages.
        # Only count right and bottom walls to avoid duplicates.
        for y in range(ROWS):
            for x in range(COLS):
                cell = self.grid[y][x]

                if x < COLS - 1 and not cell.walls["right"]:
                    passages += 1

                if y < ROWS - 1 and not cell.walls["bottom"]:
                    passages += 1

        # BFS connectivity check
        while queue:
            x, y = queue.popleft()

            if (x, y) in visited:
                continue

            visited.add((x, y))

            cell = self.grid[y][x]

            directions = [
                (0, -1, "top"),
                (1, 0, "right"),
                (0, 1, "bottom"),
                (-1, 0, "left")
            ]

            for dx, dy, direction in directions:

                if not cell.walls[direction]:
                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        if (nx, ny) not in visited:
                            queue.append((nx, ny))

        # A perfect maze is connected and has exactly
        # one fewer internal passage than the number of cells.
        connected = len(visited) == ROWS * COLS
        no_loops = passages == ROWS * COLS - 1

        return connected and no_loops

    # Draw the maze
    def draw(self, screen):

        for row in self.grid:
            for cell in row:

                x = cell.x * CELL_SIZE
                y = cell.y * CELL_SIZE

                if cell.walls["top"]:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (x, y),
                        (x + CELL_SIZE, y), 2
                    )

                if cell.walls["right"]:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (x + CELL_SIZE, y),
                        (x + CELL_SIZE, y + CELL_SIZE), 2
                    )

                if cell.walls["bottom"]:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (x + CELL_SIZE, y + CELL_SIZE),
                        (x, y + CELL_SIZE), 2
                    )

                if cell.walls["left"]:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (x, y + CELL_SIZE),
                        (x, y), 2
                    )


# ---------------- MAIN ----------------


def main():

    global GENERATION_SPEED

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hunt and Kill Maze Generator")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    maze = Maze()
    generator = maze.generate()

    generation_speed = GENERATION_SPEED

    paused = False
    accumulator = 0

    running = True

    while running:

        dt = clock.tick(FPS) / 1000

        # ---------------- EVENTS ----------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    paused = not paused

                elif event.key == pygame.K_r:
                    maze = Maze()
                    generator = maze.generate()
                    accumulator = 0
                    paused = False

                # Increase generation speed
                elif event.key == pygame.K_UP:

                    if generation_speed == 1:
                        generation_speed = 15

                    elif generation_speed == 15:
                        generation_speed = 30

                    else:
                        generation_speed = min(
                            generation_speed + 30,
                            1000
                        )

                # Decrease generation speed
                elif event.key == pygame.K_DOWN:

                    if generation_speed <= 15:
                        generation_speed = 1

                    elif generation_speed == 30:
                        generation_speed = 15

                    else:
                        generation_speed -= 30

        # ---------------- GENERATION ----------------

        if not paused and not maze.finished:

            accumulator += dt * generation_speed

            while accumulator >= 1:

                try:
                    next(generator)
                except StopIteration:
                    break

                accumulator -= 1

        # ---------------- DRAW ----------------

        screen.fill(BACKGROUND)

        maze_surface = screen.subsurface(
            (0, 0, WIDTH, MAZE_HEIGHT)
        )

        maze_surface.fill(BACKGROUND)
        maze.draw(maze_surface)

        # HUD background
        pygame.draw.rect(
            screen,
            HUD_COLOR,
            (0, MAZE_HEIGHT, WIDTH, HUD_HEIGHT)
        )

        # Status text
        if maze.finished:

            if maze.valid:
                status = "Maze Complete! - Perfect Maze Verified"
            else:
                status = "Maze Validation Failed!"

        elif paused:
            status = "PAUSED"

        else:
            status = "Generating..."

        status_text = font.render(
            status,
            True,
            TEXT_COLOR
        )

        screen.blit(
            status_text,
            (10, MAZE_HEIGHT + 5)
        )

        # Controls text
        controls = (
            f"Speed: {generation_speed} steps/sec | "
            "SPACE: Pause | R: Restart | ESC: Quit"
        )

        controls_text = font.render(
            controls,
            True,
            TEXT_COLOR
        )

        screen.blit(
            controls_text,
            (10, MAZE_HEIGHT + 27)
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
