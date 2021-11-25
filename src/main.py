import matplotlib.pyplot as plt
import numpy as np

from PCG import Map
from utility import HSV_to_RGB

# Save generated map with pyplot
def save_map(map: np.ndarray, output: str) -> None:
  print("\nConverting HSV to RGB ...")
  RGB_map = HSV_to_RGB(map)
  plt.imshow(np.clip(RGB_map, 0, 1))
  plt.axis("off")
  plt.savefig(output, bbox_inches="tight")  # Save image to file
  print("\nMap saved to", output)

# Start of script
if __name__ == "__main__":
  print("=== PROCEDURAL CONTENT GENERATION ===")
  try:
    print("Both resolutions are constrained by the perlin noise (see README)\n")
    res_X = int(input("Width of to be generated map >> "))
    res_Y = int(input("Height of to be generated map >> "))
    output = input("Output-file where generated map is saved >> ")
    if output == "": output = "out.png"  # In case empty string is given as name

    if res_X <= 0 or res_Y <= 0: # Restrictions on resolutions
      raise ValueError
  except ValueError:
    print("Error: Invalid input.")
    exit(1)

  print("\n==== Start Generation ====")
  M = Map(res_X, res_Y)
  M.generate()                   # Generate the map with the procedures
  save_map(M.get_map(), output)  # Save the map with pyplot
