class ParkingSystem:

    def __init__(self, big: int, medium: int, small: int):
        self.big = big
        self.medium = medium
        self.small = small


    def addCar(self, carType: int) -> bool:
        if carType == 1:
            if self.big > 0:
                self.big -= 1
                return True
        elif carType == 2:
            if self.medium > 0:
                self.medium -= 1
                return True
        elif carType == 3:
            if self.small > 0:
                self.small -= 1
                return True
        else:
            print('carType must be either 1, or 2 or 3')
        return False


import random

test = ParkingSystem(3, 2, 1)
for i in range(10):
    car = random.randint(1, 3)
    print('Car type {} in parking is: {}'.format(car, test.addCar(car)))
