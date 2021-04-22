import numpy as np
from utils.convert_las import convertLas
from utils.oct_tree import OctTree
from time import sleep
from tqdm import tqdm
import argparse
import os
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', help='Data File Name', default='2743_1234.las')
    parser.add_argument('--scaled_data', default=False)
    parser.add_argument('--max_type', help='"depth" or "nodes"', default='nodes')
    parser.add_argument('--max_value', default=100)
    parser.add_argument('--progressbar', default=True)
    parser.add_argument('--save_result', default=True)
    
    args = parser.parse_args()

    convert_las = convertLas(args.data_file, use_scaled_data=args.scaled_data)
    data = convert_las.las_to_xyz()
    
    min_data_point = [min(data[:, 0]), min(data[:, 1]), min(data[:, 2])]
    max_data_point = [max(data[:, 0]), max(data[:, 1]), max(data[:, 2])]
    data_map_size = max(np.array(max_data_point) - min(min_data_point))
    
    print('\n'.join([
        'Basic Data Info:',
        'Shape: %s' %', '.join([str(d) for d in data.shape]),
        'Min Coord: %s' %', '.join([str(d) for d in min_data_point]),
        'Max Coord: %s' %', '.join([str(d) for d in max_data_point]),
        'Data Map Size: %d' %data_map_size
        ])) ; sleep(0.25)

    oct_tree = OctTree(min_data_point, data_map_size, args.max_type, args.max_value)
    
    if args.progressbar:
        disable = False
    else:
        disable = True
    
    for point in tqdm(data, disable=disable):
        oct_tree.insertNode(point)

    sleep(0.25) ; print('Generated Oct Tree With %d Points' %len(data))
    
    if args.save_result:
        result = {}
        for i, x in enumerate(oct_tree.iterateDepthFirst()):
            result[','.join([str(coord) for coord in x.node_position])] = x.data_point_list
        
        pickle.dump(result, open(os.path.join(os.getcwd(), 'data', 'result.p'), 'wb'))
