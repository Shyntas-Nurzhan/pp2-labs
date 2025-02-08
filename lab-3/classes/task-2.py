class Shape:
    def init(self):
        self.area_value = 0


class Square(Shape):
    def init(self, length):
        super().init()
        
        self.length = length
        
        self.area_value = length * length

    def area(self):
        print("Area of square:", self.area_value)

user = float(input("Enter the length of the square: "))

squ = Square(user)
squ.area()