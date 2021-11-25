# Contains various utility functions

import typing
import math
import numpy as np

#======== DISTANCE BETWEEN TWO VECTORS ========
def euclidian_dist(V1: list, V2: list) -> int:
  sum = 0
  for i in range(len(V1)):
    sum += (V2[i] - V1[i])**2
  return int(math.sqrt(sum))

#======== CONVERSION OF HSV TO RGB ========
# Converts H, C and X to tuple of C, X and 0 in correct order on the basis of H
def convert(H: float, C: float, X: float) -> typing.Tuple[float, float, float]:
  if 0 <= H < 60:
    return (C, X, 0)
  elif 60 <= H < 120:
    return (X, C, 0)
  elif 120 <= H < 180:
    return (0, C, X)
  elif 180 <= H < 240:
    return (0, X, C)
  elif 240 <= H < 300:
    return (X, 0, C)
  elif 300 <= H <= 360:
    return (C, 0, X)

# Converts the HSV values to RGB, for plot purposes
def HSV_to_RGB(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  RGB_map = np.empty((res_Y, res_X, 3))

  # Divide by vector for RGB-conversion, such that S and V will be in [0, 1]
  div = np.array([1, 100, 100])

  for y in range(res_Y):
    for x in range(res_X):
      pixel = map[y][x] / div  # Divide by vector, and convert to floats

      # Convert HSV-pixel to RGB-values
      C = pixel[1] * pixel[2]
      X = C * (1 - abs((pixel[0] / 60) % 2 - 1))
      m = pixel[2] - C

      # Compute final values of RGB-pixel
      RGB_map[y][x] = convert(pixel[0], C, X) + m

  return RGB_map