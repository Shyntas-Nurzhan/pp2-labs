class Shape:
    def init(self):
        self.area_value = 0


class Rectangle(Shape):
    def init(self, length,width):
        super().init()
        
        self.length = length
        self.width = width
        
        self.area_value = length * width

    def area(self):
        print("Area of rectangle:", self.area_value)

leng = float(input("Enter the length of the rectangle: "))
widt = float(input("Enter the width of the rectangle: "))

rec = Rectangle(leng,widt)
rec.area()