#about variables


x = 5
y = "John"
print(x)
print(y)


x = 5
y = "John"
print(x)
print(y)


x = 5
y = "John"
print(type(x))
print(type(y))


#about variable names

myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"


#about assigning

myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#about output

x = "Python "
y = "is "
z = "awesome"
print(x + y + z)

#about hierarchy of variables

x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)