# Procedural Content Generation - 2D map
This project contains the code to generate a 2D-map (representing a landscape) with procedures. HSV-values are used for the pixels such that the Hue and Saturation represent the biome and the Value represents the height.

The landscape consists of: relief, 7 biomes, vegetation, villages, roads, volcanos, boats and flags. The 7 biomes are: `WATER`, `BEACH`, `GRASS`, `FOREST`, `DIRT`, `MOUNTAIN` and `SNOW`. Since the Value-component is reserved for relief, each biome is defined with a Hue and Saturation. Please note that the Hue must be _unique_ for every biome. These definitions are denoted in `/src/color.py`. At which heights every biome appears, along with other definitions, is denoted in `/src/settings.py`.

In order to generate relief, Perlin/Fractal noise is used. The implementations are in `/src/perlin2d.py` and are written by Pierre Vigier ([GitHub](https://github.com/pvigier/perlin-numpy/)).

![Example landscape](/img/progression_seed42/3_populating.png)

## Contents

*   [Generating a landscape](#landscape)
*   [Requirements](#requirements)
*   [Usage](#usage)
*   [Examples](#examples)
*   [Hierarchy](#index)

## Generating a landscape <div id="landscape"></div>
The components of the landscape are generated with the following steps:
1. **Initialize the map**;
2. **Generate relief**; Generate noise with Perlin/Fractal which represents the relief. This data is inserted in the Value component of the map. Consequently, light and dark pixels represent high and low points respectively.
3. **Add biomes to the map**; Every pixel belongs to a biome based on its Value. The `THRESHOLD` values in `/src/settings.py` denote which heights belong to which biome. Consequently, a nice gradient appears in one biome indicating the heights (e.g. the water) due to the use of Value.
4. **Add plants to the biomes**; Trees and bushes are generated in `FOREST` and `DIRT`. The probability for vegetation to spawn on a pixel for `FOREST` and `DIRT` is specified with `P_VEGETATION` and `P_VEGETATION_DIRT` respectively.
5. **Add villages to the landscape**; for every pixel is a probability `P_VILLAGE` that it becomes the origin of a village. Then, if this is case, in a radius of `SIZE_VILLAGE_X` and `SIZE_VILLAGE_Y`, for every pixel is determined whether it becomes a house (probability is `P_HOUSE`). The origin of the village is saved for later. Villages can only generate in or nearby the `GRASS` biome and not on water.
6. **Add volcanos, boats and flags**; based on their respective probabilities, volcanos, boats and flags can be generated in the map. Volcanos and flags are exclusive to the `SNOW` biome, while the boats are exclusive to `WATER`.
7. **Connect (some of) the villages with roads**; as mentioned in a previous step, the origin of every village is saved. Here, the origins are connected by road with a probability `P_ROAD`. Thereby, if the distance (Euclidian distance) between these origins is larger than `MAX_DIST`, then no road is generated. With the use of the Euclidian distance, the shortest path between the two origins is generated.

The steps mention various settings and probabilities; these are defined in `settings.py` with their effect described. There are also definitions regarding the color of biomes, houses and roads. The current settings are finetuned for a resolution of 1280x720 (720p).

## Requirements <div id="requirements"></div>
* Python (tested with v3.8)
* Matplotlib (tested with v3.3.3), only for converting the map into an image
* Numpy (tested with v1.19.5)

## Usage <div id="usage"></div>
In order to generate a landscape, simply run the following command:
```
python3 main.py
```
After this, the script asks for the horizontal and vertical resolution of the map. Then the script will generate the map and convert it into an image via matplotlib. These resolutions must meet the following criteria: they must be a multiple of `lacunarity^(octaves-1)*res`. The values for these variables are currently: `lacunarity=2, octaves=5 and res=(3,4)`. Only octaves and res are defined in `settings.py`. The current settings work for 720p. Additionally, an output file is asked, this is where the generated map (excluding the height-map) will be stored.

It is also possible to import `PCG.py` (which contains the class with which the map is generated). To create a new class instance of `Map` and generate a new map, simply use the following code:
```
M = Map(res_X, res_Y, seed)  # Create new instance of Map; seed is optional
M.generate()                 # Generate map
map = M.get_map()            # Get the HSV-map
height_map = M.get_relief()  # Get the height-map (values in range [0,100])
```
This will return the map in HSV-format. If you need the map in RGB-format, simply use the function `HSV_to_RGB` from `utility.py` in order to convert the map to RGB. Note: the seed for creating a `Map` instance is optional.

## Examples <div id="examples"></div>
The directory `img` contains multiple examples of generated landscapes. Also a progession for seed 42 is given in `progression_seed42`, here the effect of the steps is visualized. All examples are with a resolution of 1280x720.

## Hierarchy <div id="index"></div>
Here, an overview of all files of the project is given:
```
Procedural-Content-Generation/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── img
|   ├── progresion_seed42
|   |   ├── 1_relief.png
|   |   ├── 2_biomes.png
|   |   └── 3_populating.png
|   ├── example1.png
|   ├── example2.png
|   ├── example3.png
|   └── example4.png
└── src
    ├── main.py
    ├── perlin2d.py
    ├── PCG.py
    ├── color.py
    ├── settings.py
    └── utility.py
```
