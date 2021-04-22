from laspy.file import File
import os
import numpy as np

class convertLas(object):
    def __init__(self, las_f_name, use_scaled_data):
        cwd = os.getcwd()
        if 'utils' in cwd:
            cwd = os.path.split(cwd)[0]
            
        self.las_f_path = os.path.join(cwd, 'data', las_f_name)
        self.use_scaled_data = use_scaled_data
        
    def las_to_xyz(self):
        data_file = File(self.las_f_path, mode='r')
        
        if self.use_scaled_data:
            data = np.stack([data_file.x, data_file.y, data_file.z], axis=1)
        else:
            data = np.stack([data_file.X, data_file.Y, data_file.Z], axis=1)
        
        data_file.close()
        return data