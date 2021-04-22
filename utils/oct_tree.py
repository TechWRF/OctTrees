import numpy as np

class OctNode(object):
    def __init__(self, node_position, node_size, node_depth, data_point_list):
        """
        node_position is center coordinates of node
        node_size is cube width
        node_depth is number of parent cube subdivisions
        data_point_list is list of [x, y, z] of our data
        
        is_leaf_node is True by default.
        This means new nodes are children until they are subdivided
        branches are None by default because new nodes are leaf nodes
        
        lower and upper are geometrical cube boundaries
        """
        
        self.node_position = node_position
        self.node_size = node_size
        self.node_depth = node_depth
        self.data_point_list = data_point_list
        
        self.is_leaf_node = True
        self.branches = [None] * 8
        
        self.half_size = node_size / 2
        self.lower, self.upper = [], []
        for i in range(3):
            self.lower.append(node_position[i] - self.half_size)
            self.upper.append(node_position[i] + self.half_size)

    def __str__(self):
        data_str = u", ".join((str(x) for x in self.data_point_list))
        return u"position: {0}, size: {1}, depth: {2} leaf: {3}, data: {4}".format(
            self.node_position, self.node_size, self.node_depth, self.is_leaf_node, data_str
        )

class OctTree(object):
    def __init__(self, min_data_point, data_map_size, max_type, max_value):
        """        
        root is initial cube which will be subdivided by adding more datapoints
        
        max_type is either "nodes" or "depth"
        "nodes" limits number of data points in each cube
        "depth" limits number of subdivisions
        """
        
        self.root = OctNode(min_data_point, data_map_size, node_depth=0, data_point_list=[])
        self.data_map_size = data_map_size
        if max_type == 'nodes':
            self.limit_nodes = True
        else:
            self.limit_nodes = False
            
        self.limit = max_value
        
    def insertNode(self, point_position, point_data=None):
        """
        Returns Node where data point is located or 
        returns None if data point is out of boundaries
        point_data is point coordinates, later other values 
        can be added, like intensity, rgb
        """
        
        if np.any(point_position < self.root.lower) or np.any(point_position > self.root.upper):
            return None
        
        if point_data is None:
            point_data = point_position
            
        return self.__insertNode(self.root, self.root.node_size, self.root, point_position, point_data)

    def __insertNode(self, root, node_size, parent, point_position, point_data):        
        if root is None:
            """
            Root node is empty, therefore insert the data point here
            
            pos is parent node's center
            offset is new node's center
            new node's center is found by branch number
            """
            
            pos = np.array(parent.node_position)
            offset = node_size / 2
            
            branch = self.__findBranch(parent, point_position)
            
            if branch == 0:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] - offset )
            elif branch == 1:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] + offset )
            elif branch == 2:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] - offset )
            elif branch == 3:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] + offset )
            elif branch == 4:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )
            elif branch == 5:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] + offset )
            elif branch == 6:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] - offset )
            elif branch == 7:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] + offset )
                            
            return OctNode(newCenter, node_size, parent.node_depth + 1, [point_data])
        
        elif root.is_leaf_node is False and \
        np.any(root.node_position != point_position):
            """
            Node has children and point is not at center of cube node, 
            therefore point is inserted to appropriate leaf node
            """
            
            branch = self.__findBranch(root, point_position)
            new_size = root.node_size / 2
            root.branches[branch] = self.__insertNode(root.branches[branch], new_size, root, point_position, point_data)
            
        elif root.is_leaf_node:
            """
            Node is leaf node. If it has less data points than limit, add new point,
            if limit is exceeded, subdivide leaf node.
            """
            
            root.data_point_list.append(point_data)
            
            if (self.limit_nodes and len(root.data_point_list) < self.limit) or \
            (not self.limit_nodes and root.node_depth >= self.limit):
                return root
            
            else:
                point_list = root.data_point_list.copy()
                root.data = None
                root.is_leaf_node = False
                new_size = root.node_size / 2
                for point_data in point_list:
                    point_position = point_data
                    branch = self.__findBranch(root, point_position)
                    root.branches[branch] = self.__insertNode(root.branches[branch], new_size, root, point_position, point_data)

        return root

    def findPosition(self, point_position):
        """
        Returns all leaf node points or None if out of bounds
        """
        
        if np.any(point_position < self.root.lower) or np.any(point_position > self.root.upper):
            return None
        return self.__findPosition(self.root, point_position)
    
    @staticmethod
    def __findPosition(node, point_position, count=0, branch=0):
        if node.is_leaf_node:
            return node.data
        
        branch = OctTree.__findBranch(node, point_position)
        child = node.branches[branch]
        if child is None:
            return None
        
        return OctTree.__findPosition(child, point_position, count + 1, branch)
    
    @staticmethod
    def __findBranch(root, point_position):
        index = 0
        if (point_position[0] >= root.node_position[0]):
            index |= 4
        if (point_position[1] >= root.node_position[1]):
            index |= 2
        if (point_position[2] >= root.node_position[2]):
            index |= 1
        return index
    
    def iterateDepthFirst(self):
        gen = self.__iterateDepthFirst(self.root)
        for n in gen:
            yield n
            
    @staticmethod
    def __iterateDepthFirst(root):
        for branch in root.branches:
            if branch is None:
                continue
            for n in OctTree.__iterateDepthFirst(branch):
                yield n
            if branch.is_leaf_node:
                yield branch