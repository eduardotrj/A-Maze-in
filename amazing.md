

# Amazing 

## Structure:

```
maze_generator/
│
├── README.md
├── requirements.txt
├── settings.json
├── main.py
│
├── assets/  (Optional) -> graphic resources
│   ├── images/ 
│   ├── textures/
│   ├── fonts/
│   └── icons/
│
├── config/  -> Related to select and load confg.
│   ├── __init__.py
│   ├── loader.py
│   ├── validator.py
│   └── defaults.py
│
├── maze/  -> Maze data structure (Class)
│   ├── __init__.py
│   │
│   ├── model.py
│   ├── cell.py
│   ├── grid.py
│   │
│   ├── generator.py
│   ├── solver.py
│   ├── validator.py
│   └── exporter.py
│
├── algorithms/  -> Algorithms insolated.
│   ├── __init__.py
│   │
│   ├── generation/
│   │   ├── recursive_backtracker.py
│   │   ├── prim.py
│   │   ├── kruskal.py
│   │   ├── eller.py
│   │   ├── wilson.py
│   │   └── hunt_and_kill.py
│   │
│   └── solving/ /  (1)  -> Solving classes
│       ├── bfs.py
│       ├── dfs.py
│       ├── astar.py
│       ├── dijkstra.py
│       └── wall_follower.py
│
├── graphics/   ->  MiniLibX stuff (Maybe for ASCII??)
│   ├── __init__.py
│   ├── window.py
│   ├── renderer.py
│   ├── colors.py
│   ├── camera.py /  (Optional)
│   ├── events.py
│   ├── animation.py
│   └── mlx_wrapper.py
│
├── io/  (Optional) -> Exporting files (img, txt, etc)
│   ├── __init__.py
│   ├── save_png.py
│   ├── save_json.py
│   ├── load_json.py
│   └── logger.py
│
├── utils/  -> Specials to use if required.
│   ├── randomizer.py
│   ├── timer.py   /  (Optional)
│   ├── geometry.py  /  (Optional)
│   └── constants.py
│
├── tests/    (Optional)
│   ├── test_generation.py
│   ├── test_solver.py
│   ├── test_settings.py
│   └── test_renderer.py
│
└── examples/  (Optional)
    ├── tiny.json
    ├── medium.json
    └── huge.json
```

## Proccess:

1. Load settings
2. Validate settings
3. Create Grid (size)
4. Load Algorithm
5. Generate maze.
6. Generate solution.
7. Load in MiniLibX window.
8. Draw maze.
9. Draw solution
10. Listen user imputs.

## Relation Class:

```mermaid
---
title ft_printf Processing Flow
---
graph TB;
    id1([a_maze_ing.py
    Main])--Load-->Settings
    Settings-->Maze
    Maze-->Generator
    Maze-->Solver
    Generator-->Render
    Solver-->Render
    Render-->MiniLibX
    Render-->ASCII
    MiniLibX-->Listen_Events
    ASCII-->Listen_Events
```



## Duties:

- [ ] () Load Settings
- [ ] () Generate windows
- [ ] () Algorithm Gener: Recursive Backtracker
- [ ] () Algorithm Gener: Prim
- [ ] () Algorithm Gener: Kruskal
- [ ] () Algorithm Gener: eller
- [ ] () Algorithm Gener: wilson
- [ ] () Algorithm Gener: hunt_and_kill
- [ ] () Algorithm 
- [ ] () Algorithm 
- [ ] () Algorithm 
- [ ] () Algorithm 
- [ ] () Algorithm 
- [ ] () Algorithm 

- [ ] () Generate maze



MODUlE (visual)
module (parameters)
exucte|
algorithms

(OPTIONAL): Menu to change configuration inside app and save it.

## Specifications:

### Specifics
- [ ] Maze generator in Python (1 single perfect path)
- [ ] Work by reading a confg file: `config.txt`
- [ ] Write file using hexadecimal wall representation.
- [ ] Imput: `python3 a_maze_ing.py config.txt`.
- [ ] Main: `a_maze_ing.py`.
- [ ] Randomly by seeds.
- [ ] By Cells (with 0 - 4 walls)
- [ ] Entry and exit inside maze bounds.
- [ ] Coherent data generated (Related walls between cells)
- [ ] Not corridors > 2 cells.
- [ ] Not larger empty areas than 3x3.
- [ ] 42 representation (closed cells) if is space.
- [ ] PERFECT flag for generate 1 possible path.
- [ ] ASCII or MiniLibX library (Visual)
- [ ] User interactions:
    - [ ]  Re-generate new maze.
    - [ ] Show/hide shortest path.
    - [ ] Change walls colours.
    - [ ] Set color for 42

- [ ] Bonus:
    - [ ] Multiple maze generator algorithms.
    - [ ] Animations during maze generation.

### Output:

3: 0011   ─┐   A: 1010          NESW
           │e          w│  │e

ABC34BCA4  -> row inf.
BCA4ABC2A
BBC34CA4B
14BDFEEAB

1, 1      -> entry coords
5, 3      -> exit coords
SWSSENW   -> shortest path

*All ends with /n


- Cells (row by row)
- Sep by empty line: Entry, exitd coords + shortest way with NESW
### General
- [ ] Handle all possible errors (try-except)
    - Files
    - Connections
    - Inputs
    - Key catchs
    - Impossible parameters.
    - Syntax errors.
- [ ] Context managers for external resources -> Auto Cleanup
- [ ] Flake8
- [ ] Mypy --strict
- [ ] Docstrings:
    - PEP 257 (Google | NumPy style)
    - Definition functions, Class, Methods (public)
    - Designed to info when `-h` or `help`.
    - `""" Do X and return a list. """` -> Example.
    - `""" function(a, b) -> list"""` -> Only for C code.
    - Extra information: args, returns, side effects, exceptions or restrictions.
    - Use `override when subclasses remplace superclass methods.
    - Use `extend` when calls superclass method.
- [ ] Makefile:
    - `install` -> dependencies by pip, **uv**, pipx
    - `run` -> Execute main script by pip
    - `debug` -> Run in debug mode like pdb.
    - `clean` -> Remove temp files or cache (__pycache__, .mypy_cache)
    - `lint` -> Execute commands like flake8 or mypy:
        --warn-return-any
        --warn-unused-ignores 
        --ignore-missing-imports 
        --disallow-untyped-defs
        --check-untyped-defs
    - `lint-strict` -> with --strict
- [ ] pytest or unittest
- [ ] `.gitignore` for python artifacts.
- [ ] Use virtual env.
- [ ] Rehusable code (Class inside standalone module)
- [ ] Rehusable code able to pip install -> mazegen-* (allowed .tar.gz and .whl)
- [ ] Docs with:
    - [ ] Init and use maze instructions.
    - [ ] Pass custom parameters.
    - [ ] Access to generate structure and least 1 solution.
    - [ ] Structure, format of config file.
    - [ ] Maze generator algorith
    - [ ] WHy got this algorithm
    - [ ] What and how use reusable code
    - [ ] Roles for each team member
    - [ ] Anticipate planning and project development.
    - [ ] What works well and what can be improved
    - [ ] Specific tools used.




### Config Document:
Use KEY=VALUE.
#Comment inside document.

| Key | Description | Example
| :---  | :--- | :--- |
| WIDTH | Maze width (number of cells) | WIDTH=20
| HEIGHT | Maze height | HEIGHT=15
| ENTRY | Entry coordinates (x,y) | ENTRY=0,0
| EXIT | Exit coordinates (x,y) | EXIT=19,14
| OUTPUT_FILE | Output filename | OUTPUT_FILE=maze.txt
| PERFECT | Is the maze perfect? | PERFECT=True

(optional: Algorithms, display mode, seeds):

| Key | Description | Example
| :---  | :--- | :--- |
| GENERATOR | Algorithm | GENERATOR=Prim
| SEED | Seed to generate | SEED=null
| ANIMATION | Show animation | ANIMATION: True
| SPEED | Speed to show animation | SPEED=300
| WALL | Color for walls | WALL:"#000000"
| FLOOR | Color for floor | FLOOR:"#FFFFFF"
| SOLUTION | Color for solution | SOLUTION:"#00AAFF
| ENTRY | Color for entry | ENTRY:"#00FF00
| EXIT | Color for exit | EXIT:"#ff5100

### Docstring examples:

```python
def kos_root():
    """Return the pathname of the KOS root directory."""  <- Docstrings
    global _kos_root
    if _kos_root: return _kos_root
    ...
```

```python
def complex(real=0.0, imag=0.0):
    """Form a complex number.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """
    if imag == 0.0 and real == 0.0:
        return complex_zero
    ...
```

<span style="color:blue">some *blue* text</span>.

## MXL Lib:

1. Initiate lib:
```python
from mlx import Mlx
# Inititate graphic mlx (Connection with MXL)
# Return: MLX Pointer if Ok else -> None
def mlx_init() -> int: # void *

def mlx_release() -> int: # void 
```

2. Window Managing:
```python
# Create a window. Require size, tittle and MLX pointer from init.
# Return: Window Pointer if Ok else -> Null
def mlx_new_window(mlx_ptr: int, width: int, height: int, title: str ) -> int: # void *
# Clear in Black a window. Return: None
def mlx_clear_window(mlx_ptr: int, win_ptr: int) -> int:
# Close the window. Return None
def mlx_destroy_window(mlx_ptr: int, win_ptr: int ) -> int:
# *Manage multi-window
```

3. Draw:
```python
# Draw a pixel in x,y coordenates in BGRA color (0-255)
def mlx_pixel_put(mlx_ptr: int, win_ptr: int, x: int, y: int, color: int) -> int:
# Show Specific string in x,y coordenates.
def mlx_string_put(mlx_ptr: int, win_ptr: int, x: int, y: int, color: int, string: str) -> int:
# *Slow methods, better work with images.
```

4. Image Manipulation:
```python
# Add image into memory. Return -> Image Pointer (To manipulate later)
# Return Null if error.
def mlx_new_image(mlx_ptr: int, width: int, height: int) -> int: # void *
# Sent/return information about the image
def mlx_get_data_addr(img_ptr: int, bits_per_pixel: int, size_line: int, format: int) -> tuple[memoryview, int, int, int]:
# Print Image in the x,y coordenates
def mlx_put_image_to_window(mlx_ptr: int, win_ptr: int, img_ptr: int, x: int, y: int) -> int:
# Translatae images PNG into readable type with transparency
def mlx_png_file_to_image(mlx_ptr: int, filename: str) -> int: # void *
# Delete an image (pointer) Return Null if error
def mlx_destroy_image(mlx_ptr: int, img_ptr: int) -> int:
    # *Color is packing in  4-byte ARGB. 
```

5. Error Handling:
```python
# Loop to wait for events
def mlx_loop(mlx_ptr: int) -> int:
# f when a key is presset
def mlx_key_hook(win_ptr: int, callback: Callable[Any], param: Any) -> int:
# f When mouse click
def mlx_mouse_hook(win_ptr: int, callback: Callable[Any], param: Any) -> int:
#
def mlx_expose_hook(win_ptr: int, callback: Callable[Any], param: Any) -> int:
# Call f when NOT event
def mlx_loop_hook(mlx_ptr: int, callback: Callable[Any], param: Any) -> int:
def mlx_loop_exit(mlx_ptr: int) -> None:

```

6. Extra events:
```python
# Show or hide Mouse pointer
def mlx_mouse_hide(mlx_ptr: int) -> int:
def mlx_mouse_show(mlx_ptr: int) -> int:
# Move or get mouse position
def mlx_mouse_move(mlx_ptr: int, x: int, y: int) -> int:
def mlx_mouse_get_pos(win_ptr: int) -> tuple(int, int, int):
# Allow (default) or disable autorepeat -> Call event for each time
def mlx_do_key_autorepeatoff(mlx_ptr: int) -> int:
def mlx_do_key_autorepeaton(mlx_ptr: int) -> int:
# Read screen size
def mlx_get_screen_size(mlx_ptr: int) -> tuple(int, int, int):
# Flush and sync actions and functions
def mlx_do_sync(mlx_ptr: int) -> int:
def mlx_sync(mlx_ptr: int, cmd: int, img_or_win_ptr: int) -> int:
```

### Generator structure

Gnerartor:
```python
class GeneratorFactory:

    @staticmethod
    def create(name):

        generators = {

            "prim": PrimGenerator,
            "dfs": RecursiveBacktracker,
            "kruskal": KruskalGenerator
        }

        return generators[name]()
```
Use:
```python
self.generator = GeneratorFactory.create(
    self.settings.generator
)
```


## External Resources:
https://github.com/dde-fite/42_MiniLibX_Python_Manual
https://mermaid.ai/open-source/syntax/flowchart.html
https://python-tcod.readthedocs.io/en/latest/tcod/charmap-reference.html
