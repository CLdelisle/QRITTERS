# import necessary libraries
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import animation

GRID_SIZE = 100      # we'll use a (100 cell) x (100 cell) grid

# choose which pattern we want to implement
# valid values for PATTERN are: 
valid_patterns = ["SHUTTLES", "BRAIN"]
args = sys.argv
if (len(args) != 2):
    print("Please provide a pattern from the list below as an argument:") 
    print([p for p in valid_patterns])
    sys.exit()
if(args[1].upper() not in valid_patterns):
    print("Please provide a pattern from the list below as an argument:") 
    print([p for p in valid_patterns])
    sys.exit()
PATTERN = args[1].upper()

# colormap for animations
# dead cells will be black, live cells will be green
cmap = ListedColormap(["black", "lime"])

# rules for Conway's Game of Life
rules = np.array([[0,0,0,1,0,0,0,0,0],[0,0,1,1,0,0,0,0,0]])
# rules for other Life-like automata
# rules = {"life"     : np.array([[0,0,0,1,0,0,0,0,0],[0,0,1,1,0,0,0,0,0]]),
#          "highlife" : np.array([[0,0,0,1,0,0,1,0,0],[0,0,1,1,0,0,0,0,0]]),
#          "diamoeba" : np.array([[0,0,0,1,0,1,1,1,1],[0,0,0,0,0,1,1,1,1]]),
#          "daynight" : np.array([[0,0,0,1,0,0,1,1,1],[0,0,0,1,1,0,1,1,1]])}

# initialize grid
grid = np.random.choice([0], (GRID_SIZE, GRID_SIZE), p=[1])
# grid = np.zeros((GRID_SIZE, GRID_SIZE)) <- initializing using np.zeros causes issues
# why is this? I'm not sure; will look later

# initialize MPL figure
fig = plt.figure(figsize=(6,6))
ax = fig.gca()
ax.axis('off')
im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=1)

# define animate function
def animate_life(n):
    global grid
    
    # count number of live neighbors for each cell
    # the Moore neighborhood of a cell is the union of its von Neumann neighborhood...
    von_neumann_neighbors = np.roll(grid, 1, 0) + np.roll(grid, -1, 0) + \
                            np.roll(grid, 1, 1) + np.roll(grid, -1, 1)
    # ...and the four cells adjacent to it diagonally 
    diag_neighbors = np.roll(np.roll(grid, 1, 0), 1, 1) + np.roll(np.roll(grid, 1, 0), -1, 1) + \
                     np.roll(np.roll(grid, -1, 0), 1, 1) + np.roll(np.roll(grid, -1, 0), -1, 1)
    num_neighbors = von_neumann_neighbors + diag_neighbors    
    
    grid = rules[grid, num_neighbors]
    im.set_data(grid)
    return im,

# define patterns (these are the cells which are ON in the initial state of each pattern)
# maybe it would be good to automate this bit, if any further patterns would be useful
shuttle_cells = [(48,33),(48,34),(49,33),(49,34),(53,38),(53,39),(53,40),
              (48,66),(48,67),(49,66),(49,67),(53,60),(53,61),(53,62),
              (54,49),(53,49),(52,49),(52,50),(52,51),(53,51),(54,51)]
brain_cells = [(45,43),(45,44),(45,45),(45,55),(45,56),(45,57),
 (46,42),(46,44),(46,46),(46,47),(46,53),(46,54),(46,56),(46,58),
 (47,42),(47,44),(47,46),(47,54),(47,56),(47,58),
 (48,43),(48,45),(48,46),(48,48),(48,49),(48,51),(48,52),(48,54),(48,55),(48,57),
 (49,47),(49,49),(49,51),(49,53),
 (50,45),(50,47),(50,49),(50,51),(50,53),(50,55),
 (51,44),(51,45),(51,47),(51,49),(51,51),(51,53),(51,55),(51,56),
 (52,44),(52,45),(52,46),(52,49),(52,51),(52,54),(52,55),(52,56),
 (53,44),(53,45),(53,48),(53,52),(53,55),(53,56),
 (54,43),(54,48),(54,49),(54,51),(54,52),(54,57),
 (55,43),(55,57)]

init_cells = []
outfile = ""
frames = 0
if PATTERN == "SHUTTLES":
    init_cells = shuttle_cells
    outfile = "img/shuttles.gif"
    frames = 300
elif PATTERN == "BRAIN":
    init_cells = brain_cells
    outfile = "img/brain.gif"
    frames = 300 # for the Brain, this results in a perfect loop!

# bake in the pattern
for i,j in init_cells:
    grid[i, j] = 1

# make and save the animation
anim = animation.FuncAnimation(fig, animate_life, frames=frames, interval=88, blit=True)
anim.save(outfile, writer="imagemagick")