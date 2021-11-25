import numpy as np
import random
import copy
import typing

from perlin2d import generate_fractal_noise_2d
from settings import *
from color import *
from utility import euclidian_dist

# Definition of the map; contains all procedures, ordered by when they are called
class Map:
  # Initialization of the map
  def __init__(self, res_X: int, res_Y: int, seed: int = None) -> None:
    self.res_X = res_X  # Resolution of map
    self.res_Y = res_Y
    self.map = np.empty((res_Y, res_X, 3), dtype=int) # Contains the HSV-values
    self.relief = []    # Height map [0-100]

    self.origin_villages = []  # Store the origin of all villages

    self.volcano = False  # Does the map contain a volcano?
    self.snow = np.zeros((res_Y, res_X), dtype=bool)  # Contains location of the snow
   
    self.seed = seed
    random.seed(self.seed)

  # Return whether the given coordinates are on the map
  def on_map(self, x: int, y: int) -> bool:
    return 0 <= x < self.res_X and 0 <= y < self.res_Y
  
  # Start generating the map via the defined procedures
  def generate(self) -> None:
    print("Generating relief ...")
    self.__relief()
    print("Generating biomes ...")
    self.__biomes()    # Water, beach, biomes
    print("Populating the map ...")
    self.__populate()  # Vegetation, villages, roads and more
    self.__recolor()   # Give some of the biomes their correct color
    print("Generation is complete!")
  
  # Return the generated map
  def get_map(self) -> np.ndarray:
    return self.map
  
  # Return the relief of the generated map
  def get_relief(self) -> np.ndarray:
    return self.relief


  # Private methods of class

  #======== RELIEF GENERATION PROCEDURES ========
  # Here, the Value-component is used to represent the height of one pixel
  # Perlin noise is used to generate the relief
  def __relief(self) -> None:
    # Generate Perlin Noise
    noise = generate_fractal_noise_2d((self.res_Y, self.res_X), RES, OCTAVE, seed=self.seed)

    # Normalize to [0, 1], then multiply with 100 for Value (of HSV)
    self.relief = (noise - noise.min()) / (noise.max()-noise.min()) * 100

    # Copy the noise to the map
    for y in range(self.res_Y):
      for x in range(self.res_X):
        self.map[y][x][2] = self.relief[y][x]  # Value-component gets the height-value
    

  #======== BIOME GENERATION PROCEDURES ========
  # Here, the Hue- and Saturation-components are altered to represent biomes
  def __biomes(self) -> None:
    # Loop over all pixels in the map
    for y in range(self.res_Y):
      for x in range(self.res_X):
        height = self.map[y][x][2]
        # WATER biome
        if height <= WATER_THRESHOLD:
          self.map[y][x][:2] = WATER
        # BEACH biome
        elif height <= BEACH_THRESHOLD:
          self.map[y][x][:2] = BEACH
        # GRASS biome
        elif height <= GRASS_THRESHOLD:
          self.map[y][x][:2] = GRASS
        # FOREST biome
        elif height <= FOREST_THRESHOLD:
          self.map[y][x][:2] = FOREST
        # DIRT biome
        elif height <= DIRT_THRESHOLD:
          self.map[y][x][:2] = DIRT
        # MOUNTAIN biome
        elif height <= MOUNTAIN_THRESHOLD:
          self.map[y][x][:2] = MOUNTAIN
        # SNOW biome
        elif height <= SNOW_THRESHOLD:
          self.map[y][x][:2] = SNOW
          self.snow[y][x] = True
  
  # Due to the use of HSV in combination with relief, it was not possible to give each..
  # .. biome their correct color with __biomes(), so here the Value is changed for the correct color
  # But since all other transformations are finished, we can alter the Value of each pixel in the biomes
  # Moreover, the actual height is saved in self.relief, so no information is lost
  def __recolor(self) -> None:
    # Loop over all pixels in the map
    for y in range(self.res_Y):
      for x in range(self.res_X):
        # Change the color, NOTE: the lightness still indicates the height of it
        if self.map[y][x][0] == BEACH[0]:
          self.map[y][x][2] += BEACH_VALUE_OFFSET
        elif self.map[y][x][0] == DIRT[0]:
          self.map[y][x][2] += DIRT_VALUE_OFFSET
        elif self.map[y][x][0] == MOUNTAIN[0]:
          self.map[y][x][2] += MOUNTAIN_VALUE_OFFSET


  #======== POPULATE GENERATION PROCEDURES ========
  # Add various objects to the generated world (villages, roads, vegetation, etc.)
  def __populate(self) -> None:
    # Loop over all pixels in the map
    for y in range(self.res_Y):
      for x in range(self.res_X):
        hue = self.map[y][x][0] # Get unique Hue -> identify biomes
                                # Edges are cant be detected since they're smoothed
        P = random.uniform(0,1)
        if hue == FOREST[0] and P < P_VEGETATION: # Generate vegetation
          self.__vegetation(x, y)
        
        elif hue == DIRT[0] and P < P_VEGETATION_DIRT:  # Generate vegetation
          self.__vegetation(x, y)

        elif hue == GRASS[0] and P < P_VILLAGE:   # Generate village
          self.origin_villages.append([x,y])
          self.__village(x, y)
        
        elif hue == WATER[0] and P < P_BOAT:      # Generate a boat
          self.__boat(x, y)

        elif hue == SNOW[0]:
          if not self.volcano and P < P_VOLCANO:
            self.__volcano(x, y)        # Replace top of mountain with volcano
            self.__volcano_stream(x, y)
            self.volcano = True
          elif P < P_FLAG:
            self.__flag_mountain(x, y)  # Generate flag of climbers
    print("Adding roads to map ...")
    self.__roads()
  
  # Generate a boat
  def __boat(self, x: int, y: int) -> None:
    # Check if boat fits on map
    if not (self.on_map(x+LEN_SIDES, y-2*LEN_SIDES) and self.on_map(x-LEN_BOAT-LEN_SIDES, y)):
      return

    # Create the boat - bottom half
    for j in range(-LEN_SIDES, 1):
      for i in range(-LEN_BOAT+j, -j):
        self.map[y+j][x+i] = BOAT_BROWN
    # Create the boat - top half
    random_hue = random.randint(0, 100)  # Random color 
    for j in range(-LEN_SIDES+1, 1):
      for i in range(-LEN_SIDES-3, 1):
        self.map[y-LEN_SIDES-1+j][x+i] = [random_hue, 100, WATER_THRESHOLD] # Random color
    
  # Extend the volcano stream with one pixel, return the next end of the stream
  def __extend_stream(self, x: int, y: int, direction: int) -> typing.Tuple[int, int]:
    if direction == 0:    # Top-left
      x -= 1
      y -= 1
    elif direction == 1:  # Top
      y -= 1
    elif direction == 2:  # Top-right
      x += 1
      y -= 1
    elif direction == 3:  # Right
      x += 1
    elif direction == 4:  # Bottom-right
      x += 1
      y += 1
    elif direction == 5:  # Bottom
      y += 1
    elif direction == 6:  # Bottom-left
      y += 1
      x -= 1
    elif direction == 7:  # Left
      x -= 1
    if not self.on_map(x, y) or self.map[y][x][0] == FOREST[0]:
      return -1, -1  # End of the map is reached, stop

    for j in range(-1, 2):
      for i in range(-1, 2):
        if self.on_map(x+i, y+j):
          self.map[y][x][:2] = VOLCANO_COLOR[random.randint(0,2)]
    return x, y

  # Add a stream going down the volcano
  def __volcano_stream(self, x: int, y: int) -> None:
    prev = 12  # Previous direction: 12-4=8 (8 is not a direction, see __extend_stream)
    while not x == -1 or random.uniform(0,1) < P_VOLCANO_STOP: # If x == -1, end is reached
      # Determine next direction, eight surrounding pixels
      direction = random.randint(0, 8)
      if abs(direction-4) == prev: # Direction is backwards, prevent this
        direction = (direction + random.randint(0, 7)) % 8
      x, y = self.__extend_stream(x, y, direction)

  # Replace the top of the mountain with a volcano
  # This is done recursively, where self.snow is updated
  def __volcano(self, x: int, y: int) -> None:
    if not self.snow[y][x]:
      return
    self.map[y][x][:2] = VOLCANO_COLOR[random.randint(0,2)]
    self.snow[y][x] = False

    for j in range(-1, 2):
      for i in range(-1, 2):
        if self.on_map(x+i, y+j):
          if self.snow[y+j][x+i]:
            self.__volcano(x+i, y+j)
          elif self.map[y+j][x+i][2] <= MOUNTAIN_THRESHOLD:
            self.map[y+j][x+i] = VOLCANO_STONE

  # Generate flag on top of a mountain
  def __flag_mountain(self, x: int, y: int) -> None:
    # Check if flag is not outside map
    if not (self.on_map(x, y+4) and self.on_map(x+3, y-3)):
      return
    # Draw the flag
    for j in range(y-3, y+5):
      self.map[j][x] = FLAG_BLACK
    self.map[y-1][x+1] = FLAG_RED
    self.map[y-1][x+2] = FLAG_RED
    self.map[y-1][x+3] = FLAG_RED
    self.map[y-2][x+1] = FLAG_RED
    self.map[y-2][x+2] = FLAG_RED
    self.map[y-2][x+3] = FLAG_RED

  # Generate some vegetation (bushes/trees)
  def __vegetation(self, x: int, y: int) -> None:
    for j in range(-3, 0):
      for i in range(-3, 0):
        if self.on_map(x+i, y+j):
          self.map[y+j][x+i] = PLANT
    if random.randint(0,1) == 0 and self.on_map(x-2, y): # Generate a trunk
      self.map[y][x-2] = TRUNK
      
  # Generate a house
  def __house(self, x: int, y: int) -> None:
    for j in range(-SIZE_HOUSE, 1):
      for i in range(-SIZE_HOUSE, 1):
        if self.on_map(x+i, y+j) and not self.map[y+j][x+i][0] == WATER[0]: # Not on water
          self.map[y+j][x+i] = HOUSE

  # Generate a village with origin (x,y)
  def __village(self, x: int, y: int) -> None:
    self.__house(x-SIZE_HOUSE, y-SIZE_HOUSE) # Origin is always a house
    for j in range(-SIZE_VILLAGE_Y, SIZE_VILLAGE_Y):
      for i in range(-SIZE_VILLAGE_X, SIZE_VILLAGE_X):
        if random.uniform(0,1) < P_HOUSE: # Generate a house
          self.__house(x+i, y+j)


  #======== ROAD GENERATION PROCEDURES ========
  # Randomly select which villages are connected with each other
  def __roads(self) -> None:
    for j in range(len(self.origin_villages)):
      for i in range(j+1, len(self.origin_villages)):
        V1, V2 = self.origin_villages[i], self.origin_villages[j]
        if random.uniform(0,1) < P_ROAD and euclidian_dist(V1, V2) <= MAX_DIST:
          self.__connect(V1, V2) # Connect the villages V1 and V2 with road
  
  # Connect the two given villages
  def __connect(self, start: list, end: list) -> None:
    x, y = start[0], start[1] # Starting point
    while not [x, y] == end:  # Destination not reached yet
      color = BRIDGE if self.map[y][x][2] < WATER_THRESHOLD else ROAD
      if self.on_map(x, y):
        self.map[y][x] = color
      
      x, y = self.__get_next_pixel(x, y, end)
      if x == -1:  # No pixels left, unable to create road. Road ends here
        break
  
  # Get the next pixel to continue road with, this pixel has shortest distance to end
  def __get_next_pixel(self, x: int, y: int, end: list) -> typing.Tuple[int, int]:
    best_dist = MAX_DIST
    next_x, next_y = -1, -1
    for j in range(-1, 2):
      for i in range(-1, 2):
        if i == 0 and j == 0:  # Skip current pixel
          continue
        # Roads have to avoid the mountains
        if self.on_map(x+i, y+j) and self.map[y+j][x+i][2] <= DIRT_THRESHOLD:
          dist = euclidian_dist([x+i, y+j], end)
          if dist < best_dist:
            best_dist = dist
            next_x, next_y = x+i, y+j
    return next_x, next_y