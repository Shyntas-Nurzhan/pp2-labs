def convert(grams):
    return int(28.3495231 * grams)
print("Hey! I am going to make a dish, but recipes states in gramms and also in Farenheits\n")
def farenheit(F):
    return int((5 / 9) * (F-32))
print("Firstly, convert me into ounces")
grams = int(input())
F = int(input("Next, convert me into Celcium: "))
print(convert(grams), "ounces and", farenheit(F),"C")