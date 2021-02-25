


class Pose:
    def __init__(self, data):
        self.nose = data[0]['position']


        # Init List, 0 for left and 1 for right
        self.hips = [0, 1]
        self.knees = [0, 1]
        self.ankles = [0, 1]
        self.scores = [0, 1]
        self.shoulders = [0, 1]

        self.shoulders[0] = data[5]
        self.shoulders[1] = data[6]
        self.hips[0] = data[11]
        self.hips[1] = data[12]
        self.knees[0] = data[13]
        self.knees[1] = data[14]
        self.ankles[0] = data[15]
        self.ankles[1] = data[16]

        # Calculate coord scores to choose the direction of body-parts
        self.scores[0] = sum(map(lambda x: x['score'], [self.shoulders[0], self.hips[0], self.knees[0], self.ankles[0]]))
        self.scores[1] = sum(map(lambda x: x['score'], [self.shoulders[1], self.hips[1], self.knees[1], self.ankles[1]]))

        if self.scores[0] > self.scores[1]:
            self.shoulder = self.shoulders[0]['position']
            self.hip = self.hips[0]['position']
            self.knee = self.knees[0]['position']
            self.ankle = self.ankles[0]['position']

        if self.scores[0] < self.scores[1]:
            self.shoulder = self.shoulders[1]['position']
            self.hip = self.hips[1]['position']
            self.knee = self.knees[1]['position']
            self.ankle = self.ankles[1]['position']
        
        self.shoulders = list(map(lambda x: x['position'], self.shoulders))
        self.hips = list(map(lambda x: x['position'], self.hips))
        self.knees = list(map(lambda x: x['position'], self.knees))
        self.ankles = list(map(lambda x: x['position'], self.ankles))