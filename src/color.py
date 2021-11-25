# Contains the definitions of all colors, in the HSV color space
# If only one or two components are defined, then a comment will specify which they are
# NOTE: each Hue must be unique in order to identify it

# Only use integers with a range of [0,360] for Hue and [0,100] for Saturation and Value

from settings import WATER_THRESHOLD


#======== BIOMES ========
# COLOR DEF: (Hue, Saturation) | Here, Value is based on the relief
WATER = [206, 100]
BEACH = [35, 38]
GRASS = [133, 100]
FOREST = [135, 50]
DIRT = [20, 57]
MOUNTAIN = [2, 7]
SNOW = [16, 20]

# After the generation is finished, change the Value for more realistic colors
BEACH_VALUE_OFFSET = 40
DIRT_VALUE_OFFSET = -20
MOUNTAIN_VALUE_OFFSET = -50


#======== MISC. ========
PLANT = [100, 100, 40]
TRUNK = [12, 50, 36]   # Trunk of tree

HOUSE = [0, 100, 40]
ROAD = [1, 0, 0]
BRIDGE = [17, 64, WATER_THRESHOLD]

# FLAG on top of a snowy mountain
FLAG_RED = [3, 100, 100]
FLAG_BLACK = [2, 100, 0]

# Lava/magma of vulcano
VOLCANO_COLOR = [[5, 89], [7, 89], [11, 89]]  # [Hue, Saturation]
VOLCANO_STONE = [4, 0, 50]

# Underside of boat
BOAT_BROWN = [27, 77, 28]