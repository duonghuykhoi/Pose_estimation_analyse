from get_angle import get_angle


STAND = 'STAND'
MIDDLE = 'MIDDLE'
SIT = 'SIT'


class Posture:

    def __init__(
            self,
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
    ):
        self.nose_standing_standard_value   = nose_standing_standard_value
        self.hip_standing_standard_value    = hip_standing_standard_value
        self.nose_standing_standard_ratio_value   = nose_standing_standard_ratio_value
        self.hip_standing_standard_ratio_value    = hip_standing_standard_ratio_value
        self.nose_sit_standard_ratio_value        = nose_sit_standard_ratio_value
        self.hip_sit_standard_ratio_value         = hip_sit_standard_ratio_value
        self.nose_sit_standard_value        = nose_sit_standard_value
        self.hip_sit_standard_value         = hip_sit_standard_value
        self.knee_sit_standard_value        = knee_sit_standard_value
        self.ankle_sit_standard_value        = ankle_sit_standard_value
    

    def get_posture(self, data):
        #Calculate angle
        squat_knee_angle = get_angle(data.hip, data.knee, data.ankle)
        squat_hip_angle = get_angle(data.shoulder, data.hip, data.knee)
        squat_hip_angle2 = get_angle(data.shoulder, data.hip, data.ankle)
        
        #Sitting condition
        if      squat_knee_angle < 90 and \
                data.nose['x'] > self.hip_standing_standard_value - (self.hip_standing_standard_value - self.nose_standing_standard_value)*0.2 and \
                data.hip['x'] > (self.hip_standing_standard_value + self.hip_sit_standard_value) / 2:
            
            return SIT


        if      data.hip['x'] - data.knee['x'] > self.hip_sit_standard_value - self.knee_sit_standard_value and \
                data.nose['x'] > self.hip_standing_standard_value - (self.hip_standing_standard_value - self.nose_standing_standard_value)*0.2 and \
                data.hip['x'] > (self.hip_standing_standard_value + self.hip_sit_standard_value) / 2:
            
            return SIT
        
    
        if      data.ankle['x'] - data.nose['x'] < self.ankle_sit_standard_value - (self.nose_sit_standard_value*2 + self.nose_standing_standard_value)/3 and \
                data.nose['x'] > self.hip_standing_standard_value - (self.hip_standing_standard_value - self.nose_standing_standard_value)*0.2 and \
                data.hip['x'] > (self.hip_standing_standard_value + self.hip_sit_standard_value) / 2:
            
            return SIT

        #Can delete it if the result wrong (line 64 to 67)
        if      (data.nose['x'] / data.ankle['x'] > self.nose_sit_standard_ratio_value or \
                data.hip['x'] / data.ankle['x'] > self.hip_sit_standard_ratio_value) and squat_hip_angle < 70 :
            
            return SIT
        #

        if      squat_hip_angle < 70   and \
                abs(data.hip['x'] - data.ankle['x']) / abs(data.nose['x'] - data.ankle['x']) < 0.35:
            
            return SIT


        #Standing condition
        if      data.nose['x'] / data.ankle['x'] < self.nose_standing_standard_ratio_value or \
                data.hip['x'] / data.ankle['x'] < self.hip_standing_standard_ratio_value:
            
            return STAND


        if      squat_hip_angle > 165  and squat_hip_angle2 > 160 and \
                abs(data.hip['x'] - data.ankle['x']) / abs(data.nose['x'] - data.ankle['x']) > 0.5:
            
            return STAND


        if data.nose['x'] < (self.nose_standing_standard_value*2 + self.hip_standing_standard_value)/3:
            
            return STAND
        
        
        return MIDDLE
