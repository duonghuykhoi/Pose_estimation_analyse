import argparse

from counter import Counter
from data import Data
from get_standard_value import get_standard_value
from posture import Posture

parser = argparse.ArgumentParser()
parser.add_argument('--input_json_path', type=str, default='./json/Squat_Video1.json')
args = parser.parse_args()

DATA_PATH = args.input_json_path

STAND = 'STAND'
MIDDLE = 'MIDDLE'
SIT = 'SIT'



def main():
    data = Data(DATA_PATH)
    counter = Counter()

    #Side of body-parts (1: right -- 0: left)
    side = sum(map(lambda x: x.scores[1] - x.scores[0], data.data))
    side = int(side > 0)

    #Standar values when standing
    nose_standing_standard_value, nose_standing_standard_ratio_value = get_standard_value(zip(map(lambda x: x.nose['x'], data.data), map(lambda x: x.ankles[side]['x'], data.data)))
    hip_standing_standard_value, hip_standing_standard_ratio_value = get_standard_value(zip(map(lambda x: x.hips[side]['x'], data.data), map(lambda x: x.ankles[side]['x'], data.data)))

    #Standar values when sitting
    nose_sit_standard_value, nose_sit_standard_ratio_value = get_standard_value(zip(map(lambda x: -x.nose['x'], data.data), map(lambda x: -x.ankles[side]['x'], data.data)))
    hip_sit_standard_value, hip_sit_standard_ratio_value = get_standard_value(zip(map(lambda x: -x.hips[side]['x'], data.data), map(lambda x: -x.ankles[side]['x'], data.data)))
    knee_sit_standard_value, knee_sit_standard_ratio_value = get_standard_value(zip(map(lambda x: -x.knees[side]['x'], data.data), map(lambda x: -x.ankles[side]['x'], data.data)))
    ankle_sit_standard_value, ankle_sit_standard_ratio_value = get_standard_value(zip(map(lambda x: -x.ankles[side]['x'], data.data), map(lambda x: -x.ankles[side]['x'], data.data)))


    posture = Posture(
            nose_standing_standard_value,
            hip_standing_standard_value,
            nose_standing_standard_ratio_value,
            hip_standing_standard_ratio_value,
            nose_sit_standard_ratio_value,
            hip_sit_standard_ratio_value,
            nose_sit_standard_value,
            hip_sit_standard_value,
            knee_sit_standard_value,
            ankle_sit_standard_value,
    )


    for i in data.data:
        pos = posture.get_posture(i)
        counter.update(pos)
    
    print(f'Total Squat Counted: {counter.count}')





if __name__ == '__main__':
    main()