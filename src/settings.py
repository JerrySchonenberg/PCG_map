# Contains definitions for the generation of content (e.g. probabilities, sizes)
# For the colors, see color.py
# NOTE: all probabilities are in [0,1]

#======== BIOMES ========
N_BIOMES = 7  # Number of biomes

# Which heights belong to what biome? (PREV_THRESHOLD < x <= THRESHOLD)
# E.g.: pixel x belongs to BEACH when WATER_THRESHOLD < x <= BEACH_THRESHOLD
# All thresholds are integers in [0,100]
WATER_THRESHOLD = 37     # Water-level
BEACH_THRESHOLD = 42     # Beach surrounding the water
GRASS_THRESHOLD = 50     # Grass level
FOREST_THRESHOLD = 75    # Forest level
DIRT_THRESHOLD = 80      # Dirt level
MOUNTAIN_THRESHOLD = 96  # Mountain level
SNOW_THRESHOLD = 100     # Snow/vulcano level


#======== PROBABILITIES ========
#PLANTS
P_VEGETATION = 0.05        # Prob. to generate vegetation
P_VEGETATION_DIRT = 0.005  # Prob. on dirt
#VILLAGES
P_HOUSE = 0.05             # Prob. of house at a pixel
P_VILLAGE = 0.0003         # Prob. of generating a village
P_ROAD = 0.04              # Prob. of connecting two villages
#MOUNTAINS
P_FLAG = 0.001             # Prob. of generating a flag
P_VOLCANO = 0.3            # Prob. of generating a volcano
P_VOLCANO_STOP = 0.001     # Prob. to stop the stream of lava
#BOATS
P_BOAT = 0.00005           # Prob. of generating a boat


#======== PERLIN/FRACTAL NOISE ========
OCTAVE = 5
RES = (3,4)


#======== MISC. ========
SIZE_VILLAGE_X = 7   # Max possible width  (= SIZE_VILLAGE_X*2) of village
SIZE_VILLAGE_Y = 7   # Max possible height (= SIZE_VILLAGE_Y*2) of village
SIZE_HOUSE = 2

MAX_DIST = 128  # Max distance between two villages to create road between them
                # (Euclidian distance)

LEN_BOAT = 10   # Length of underside of boat (in pixels)
LEN_SIDES = 5   # Length of diagonal part of boat (in pixels)