
# 🧩 Maze Hunt and Kill

A Python maze generator built using **Pygame** and the **Hunt and Kill algorithm**.

Watch randomly generated perfect mazes come to life in real time. Control the generation speed, pause the process, and generate new mazes whenever you want.

## ✨ Features

- **Hunt and Kill Algorithm** – Generates random perfect mazes.
- **Real-time Visualization** – Watch the maze being generated step by step.
- **Adjustable Speed** – Control the maze generation speed.
- **Pause and Resume** – Pause or continue generation at any time.
- **Restart** – Generate a completely new maze.
- **Maze Validation** – Uses Breadth-First Search (BFS) to verify maze connectivity and ensure there are no loops.

## 🛠️ Built With

- Python
- Pygame

## 📥 Getting Started

### Prerequisites

- Python 3.x
- Pygame

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Kaushik-Daksh/Maze_Hunt_and_Kill.git
```

**2. Navigate to the project directory**

```bash
cd Maze_Hunt_and_Kill
```

**3. Install Pygame**

```bash
pip install pygame
```

**4. Run the project**

```bash
python maze_algorithm.py
```

## 🎮 Controls

| Key | Action |
|:---:|---|
| `↑` | Increase generation speed |
| `↓` | Decrease generation speed |
| `SPACE` | Pause / Resume |
| `R` | Restart maze generation |
| `ESC` | Quit |

### Generation Speed

The generation speed follows this sequence:

`1 → 15 → 30 → 60 → 90 → 120 → ...`

The generation speed is measured in steps per second, independently of the rendering FPS.

## 🧠 Algorithm: Hunt and Kill

The Hunt and Kill algorithm is a randomized maze-generation algorithm that works in two phases.

### 1. Kill Phase

- Start at the initial cell.
- Mark the current cell as visited.
- Randomly choose an unvisited neighboring cell.
- Remove the wall between the current cell and the chosen neighbor.
- Move to that neighbor.
- Repeat until there are no unvisited neighboring cells.

### 2. Hunt Phase

- Scan the grid for an unvisited cell with at least one visited neighbor.
- Randomly select one of its visited neighbors.
- Remove the wall between the two cells.
- Return to the Kill Phase from the newly discovered cell.

These phases repeat until every cell has been visited.

## 🧪 Maze Validation

The generated maze is checked using **Breadth-First Search (BFS)**.

A perfect maze must satisfy two conditions:

1. Every cell must be reachable from every other cell.
2. The maze must contain exactly `N - 1` internal passages, where `N` is the total number of cells.

This ensures that the maze is connected and contains no loops, meaning there is exactly one path between any two cells.

## ⚙️ Configuration

You can modify the following constants in `maze_algorithm.py`:

| Variable | Default | Description |
|---|---:|---|
| `CELL_SIZE` | `30` | Size of each cell in pixels |
| `COLS` | `25` | Number of columns |
| `ROWS` | `18` | Number of rows |
| `FPS` | `60` | Rendering frame rate |
| `GENERATION_SPEED` | `120` | Initial generation speed |

## 📁 Project Structure

```text
Maze_Hunt_and_Kill/
│
└── maze_algorithm.py
└── README.md
```

## 🚀 Future Scope

There are plenty of possibilities for expanding this project:

- [ ] **Maze Solving** – Implement algorithms like BFS, DFS, and A* to automatically solve generated mazes.
- [ ] **Playable Mazes** – Allow users to navigate through generated mazes using keyboard controls.
- [ ] **Color Themes** – Introduce customizable colors, backgrounds, and visual themes.
- [ ] **Adjustable Dimensions** – Allow users to change the maze size.
- [ ] **Difficulty Settings** – Generate mazes with different sizes and configurations.
- [ ] **Generation Statistics** – Display generation time, visited cells, and other useful statistics.
- [ ] **Save and Export** – Export generated mazes as images.
- [ ] **Step-by-Step Visualization** – Improve visualization of the algorithm's Kill and Hunt phases.

## 📜 License

This project is open source. Feel free to explore, modify, and learn from it.
