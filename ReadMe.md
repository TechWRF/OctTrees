Subdivides point cloud data in LAS format using octree.

Requirements:
laspy
tqdm

1. Pull this repository
2. Place the '2743_1234.las' under 'data' directory
3. Run run.py file using python 3.x with arguments if you wish (good to go with default args):
    --data_file (your input .las file)
    --scaled_data (True/False use scaled data or use original)
    --max_type (Octree build limit mode, possible modes: 'depth' and 'nodes'. Nodes will limit number of data points in each cube, whereas Depth will limit number of subdivisions.
    --max_value (A number, corresponding to chosen --max_type)
    --progressbar (enables nice little progressbar)
    --save_result (save subdivision result as pickled dictionary under 'data' directory. Keys are cube coordinates, values are lists of data point coordinates)
    
    
Most part of code is borrowed from
https://github.com/jcummings2/pyoctree
