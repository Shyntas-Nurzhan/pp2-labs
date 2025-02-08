class StringManipulator:
    def init(self):
        self.txt = ""

    def getString(self):
        self.txt = input("Enter a string: ")

    def printString(self):
        print(self.txt.upper())

string_obj = StringManipulator()
string_obj.getString()
string_obj.printString()