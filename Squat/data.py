
import json

from pose import Pose



class Data:

    def __init__(self, data_path):
        with open(data_path) as file:
            parsed_data = json.load(file)['data']
            self.data = list(map(lambda x: Pose(x[0]['keypoints']), parsed_data))
