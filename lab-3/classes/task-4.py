import math

class Point:
    def init(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"Point coordinates: ({self.x}, {self.y})")

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        print(f"Point moved to: ({self.x}, {self.y})")

    def dist(self, other_p):
        distance = math.sqrt((other_p.x - self.x) ** 2 + (other_p.y - self.y) ** 2)
        return distance

p1 = Point(3, 4)
p2 = Point(7, 1)

p1.show()
p2.show()

p1.move(6, 8)  

print("Distance between p1 and p2:", p1.dist(p2)) 