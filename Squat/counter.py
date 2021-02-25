


STAND = 'STAND'
MIDDLE = 'MIDDLE'
SIT = 'SIT'



class Counter:

    def __init__(self):
        self.count = 0
        self.init = True
        self.flag = True

    
    def update(self, posture):
        dictionary = {
            STAND: self.stand,
            MIDDLE: self.middle,
            SIT: self.sit,
        }
        dictionary[posture]()
    

    def middle(self):
        pass


    def stand(self):
        if self.init:
            self.init = False

        if not self.flag:
            self.count += 0.5
            self.flag = True


    def sit(self):
        if self.init:
            self.count -= 0.5
            self.init = False
        
        if self.flag:
            self.count += 0.5
            self.flag = False
    
